from pathlib import Path
from typing import Protocol

from app.application.models.entities import ScreenerResult


# TODO: Maybe I need to refactor/divide this port/method to have multiple ports for different use cases
class StockScreenerPort(Protocol):
    def scan(
        self,
        filters: dict,
        db_path: Path,
        table_name: str = "screener_results",
        **kwargs,
    ) -> ScreenerResult:
        ...


    # def save_to_sqlite(
    #     self,
    #     stocks: List[Stock],
    #     db_path: Path,
    #     table_name: str = "screener_results",
    # ) -> None:
    #     ...

    # def save_to_csv(
    #     self,
    #     file_path: str,
    #     **kwargs,
    # ) -> None:
    #     ...