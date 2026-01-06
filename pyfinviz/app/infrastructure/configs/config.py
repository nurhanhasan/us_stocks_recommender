from pathlib import Path

from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    news_date_today: bool = True

    # Define absolute path to the SQLite database file
    # Default value is screener_results.db in app/db_results/screener_results.db
    db_path: str = str(Path(__file__).resolve().parents[3] / "db_results" / "screener_results.db")
    db_table_name: str = "screener_results"

configs = Configs()