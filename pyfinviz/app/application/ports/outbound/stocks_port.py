from typing import Protocol

from app.application.models.entities import AllStocks


class AllStocksPort(Protocol):
    def execute(self) -> AllStocks:
        ...

class DeleteStocksPort(Protocol):
    def execute(self) -> None:
        ...