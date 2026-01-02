import sqlite3
from enum import Enum
from pathlib import Path
from typing import List, TypedDict

import pandas as pd

from pyfinviz.screener import Screener


# Add a wrapper to extend Screener functionalities
class ScreenerWrapper:

    class ScreenerFilterOption:
        ALL = ""

    class ExtendedOrderBy(Enum):
        LATEST_NEWS = "-newstime"

    class ExtendedCustomSettingsOption(Enum):
        NEWS_TIME = "135"
        NEWS_TITLE = "137"

    class NewsOption(ScreenerFilterOption, Enum):
        TODAY = "news_date_today"
        AFTERMARKET_TODAY = "news_date_todayafter"
        SINCE_YESTERDAY = "news_date_sinceyesterday"
        SINCE_AFTERMARKET_YESTERDAY = "news_date_sinceyesterdayafter"
        YESTERDAY = "news_date_yesterday"
        YESTERDAY_AFTERMARKET = "news_date_yesterdayafter"
        LAST_5_MINUTES = "news_date_prevminutes5"
        LAST_30_MINUTES = "news_date_prevminutes30"
        LAST_1_HOUR = "news_date_prevhours1"
        LAST_24_HOURS = "news_date_prevhours24"
        LAST_7_DAYS = "news_date_prevdays7"
        LAST_1_MONTH = "news_date_prevmonth"
        CUSTOM_ELITE_ONLY = "modal"

    def __init__(self):
        self._screener = Screener()


class ChangeSummary(TypedDict):
    inserted: List[dict]
    updated: List[dict]
    unchanged: List[dict]


class PersistableScreener(Screener):

    def to_csv(self, file_path: str = "screener_results.csv", **kwargs) -> None:
        """
        Create a combined CSV with all pages concatenated (if there are multiple pages).

        :param file_path: The path where the CSV file will be saved.
        """

        all_pages: List[pd.DataFrame] = [
            df for df in self.data_frames.values() if df is not None and not df.empty
        ]

        if all_pages:
            combined = pd.concat(all_pages, ignore_index=True)
            combined.to_csv(file_path, index=False, **kwargs)


    def to_updated_deduplicated_sqlite(
        self,
        db_path: Path | None = None,
        table_name: str = "screener_results",
        **kwargs,
    ) -> ChangeSummary:
        """
        Create or update a SQLite database with all pages concatenated (if there are multiple pages).

        :param db_path: The path where the SQLite database file will be saved.
        :param table_name: The name of the table to store the results.
        """

        changes: ChangeSummary = {
            "inserted": [],
            "updated": [],
            "unchanged": [],
        }

        all_pages: List[pd.DataFrame] = [
            df for df in self.data_frames.values() if df is not None and not df.empty
        ]

        if not all_pages:
            # print("No data to write to database.")
            return {"inserted": [], "updated": [], "unchanged": []}

        # Combine pages, if multiple, before table creation.
        combined = (
            pd.concat(all_pages, ignore_index=True) if all_pages else pd.DataFrame()
        )

        if db_path is None:
            base_dir = Path(__file__).parent.parent.resolve()
            db_path = (base_dir / "db" / "screener_results.db").resolve()
        else:
            db_path = Path(db_path).resolve()


        db_file_is_missing = not db_path.exists()

        with sqlite3.connect(db_path) as conn:

            if db_file_is_missing:
                # Create table from screener view headers if it doesn't exist.
                combined.head(0).to_sql(table_name, conn, index=False, **kwargs)
                # print(f"Created new table '{table_name}' in database '{db_path}'.")

            # Loop over all dataframes, check for existing tickers, update or insert
            for df in all_pages:
                # prepare column lists for this dataframe
                cols = list(df.columns)
                safe_cols = [f'"{c}"' for c in cols]
                set_cols = [c for c in cols if c != "Ticker"]
                safe_set_cols = [f'"{c}"' for c in set_cols]

                for _, row in df.iterrows():
                    ticker = row["Ticker"]
                    existing = pd.read_sql_query(
                        f'SELECT * FROM "{table_name}" WHERE "Ticker" = ?',
                        conn,
                        params=(ticker,),
                    )

                    # Insert new row
                    if existing.empty:
                        # Insert new row (ensure order of values matches df.columns)
                        placeholders = ", ".join(["?"] * len(cols))
                        cols_sql = ", ".join(safe_cols)
                        values = [row[c] for c in cols]
                        conn.execute(
                            f'INSERT INTO "{table_name}" ({cols_sql}) VALUES ({placeholders})',
                            tuple(values),
                        )

                        changes["inserted"].append(row.to_dict())

                    # Update existing row
                    else:
                        if row.get("NewsTitle") == existing["NewsTitle"].values[0]:
                            continue  # No changes, skip update

                        # update existing row: set all columns except Ticker
                        set_clause = ", ".join([f"{c} = ?" for c in safe_set_cols])
                        values = [row[c] for c in set_cols]
                        values.append(ticker)  # WHERE parameter
                        conn.execute(
                            f'UPDATE "{table_name}" SET {set_clause} WHERE "Ticker" = ?',
                            tuple(values),
                        )
                        changes["updated"].append(row.to_dict())

        # print(
        #     f"Wrote/Updated results to {db_path} ({len(combined)} rows, {len(combined.columns)} columns) to table '{table_name}'"
        # )

        return changes
