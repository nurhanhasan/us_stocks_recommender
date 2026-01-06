import sqlite3

from app.application.models.entities import AllStocks, Stock
from app.application.ports.outbound.stocks_port import (AllStocksPort,
                                                        DeleteStocksPort)

class SqliteAllStocksRepository(AllStocksPort):
    def __init__(self, db_path: str, db_table_name: str):
        self.db_path = db_path
        self.db_table_name = db_table_name

    def execute(self) -> AllStocks:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Ensure the table exists or handle error, for now assuming it exists based on previous code
        try:
            cursor.execute("SELECT * FROM {}".format(self.db_table_name))
            stocks = cursor.fetchall()
        except sqlite3.OperationalError:
            # Table might not exist yet if scraper hasn't run
            stocks = []
        finally:
            conn.close()

        # Convert tuples to Stock objects
        # Assuming table columns align with Stock fields:
        # ticker, company, country, sector, industry, shares_float, short_interest, relative_volume, volume, price, change, news_time, news_title
        stock_entities = []
        for row in stocks:
            # Ensure row has enough elements to unpack
            if len(row) >= 13:
                stock = Stock(
                    ticker=row[0],
                    company=row[1],
                    country=row[2],
                    sector=row[3],
                    industry=row[4],
                    shares_float=row[5],
                    short_interest=row[6],
                    relative_volume=row[7],
                    volume=row[8],
                    price=row[9],
                    change=row[10],
                    news_time=row[11],
                    news_title=row[12],
                )
                stock_entities.append(stock)

        return AllStocks(stocks=stock_entities)


class SqliteDeleteStocksRepository(DeleteStocksPort):
    def __init__(self, db_path: str, db_table_name: str):
        self.db_path = db_path
        self.db_table_name = db_table_name

    def execute(self) -> None:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM {}".format(self.db_table_name))
            conn.commit()
        except sqlite3.OperationalError:
            # Table might not exist yet if scraper hasn't run
            pass
        finally:
            conn.close()
