from app.application.models.entities import AllStocks, Stock
from app.application.ports.outbound.pyfinviz_port import StockScreenerPort
from app.application.ports.outbound.stocks_port import (AllStocksPort,
                                                        DeleteStocksPort)


class ScreenerUseCase:
    """
    Run the PyFinviz stock screener and return the list of stocks.
    """
    def __init__(self, screener: StockScreenerPort):
        self.screener = screener

    def execute(self) -> list[Stock]:
        return self.screener.scan()


class AllStocksUseCase:
    """
    Returns the list of stocks in the database.
    """
    def __init__(self, stock_repository: AllStocksPort):
        self.stock_repository = stock_repository

    def execute(self) -> AllStocks:
        return self.stock_repository.execute()


class DeleteStocksUseCase:
    """
    Delete all stocks from the database.
    """
    def __init__(self, stock_repository: DeleteStocksPort):
        self.stock_repository = stock_repository

    def execute(self) -> None:
        self.stock_repository.execute()
