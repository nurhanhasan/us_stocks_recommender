from fastapi import Depends

from app.adapters.outbound.datastore.datastore_adapter import (
    SqliteAllStocksRepository, SqliteDeleteStocksRepository)
from app.adapters.outbound.pyfinviz.pyfinviz_adapter import ExtendedScreener
from app.application.models.entities import AllStocks
from app.application.ports.outbound.stocks_port import (AllStocksPort,
                                                        DeleteStocksPort)
from app.application.services.stock_screener_use_cases import (
    AllStocksUseCase, DeleteStocksUseCase, ScreenerUseCase)
from app.infrastructure.configs.config import configs
from pyfinviz.screener import Screener


# Run screener
def get_screener_adapter() -> ExtendedScreener:
    # 1. Configure the Filter Options
    options = [
        Screener.PriceOption.USD1_TO_USD20,
        Screener.RelativeVolumeOption.OVER_5,
        Screener.ChangeOption.UP_10_PERCENT,
        Screener.FloatOption.UNDER_20M,
    ]

    if configs.news_date_today:
        options.append(ExtendedScreener.NewsOption.TODAY)

    # 2. Configure Custom Settings (for the view columns)
    custom_settings_options = [
        Screener.CustomSettingsOption.NO,
        Screener.CustomSettingsOption.TICKER,
        Screener.CustomSettingsOption.COMPANY,
        Screener.CustomSettingsOption.COUNTRY,
        Screener.CustomSettingsOption.SECTOR,
        Screener.CustomSettingsOption.INDUSTRY,
        Screener.CustomSettingsOption.SHARES_FLOAT,
        Screener.CustomSettingsOption.SHORT_INTEREST,
        Screener.CustomSettingsOption.RELATIVE_VOLUME,
        Screener.CustomSettingsOption.VOLUME,
        Screener.CustomSettingsOption.PRICE,
        Screener.CustomSettingsOption.CHANGE,
        ExtendedScreener.ExtendedCustomSettingsOption.NEWS_TIME,
        ExtendedScreener.ExtendedCustomSettingsOption.NEWS_TITLE,
    ]

    # 3. Instantiate the concrete Adapter
    return ExtendedScreener(
        filter_options=options,
        view_option=Screener.ViewOption.CUSTOM_WITH_FILTERS,
        order_by=ExtendedScreener.ExtendedOrderBy.LATEST_NEWS,
        custom_settings_options=custom_settings_options,
    )

def get_screen_stocks_use_case(
    adapter: ExtendedScreener = Depends(get_screener_adapter)
    ) -> ScreenerUseCase:
    return ScreenerUseCase(screener=adapter)



# List stocks use case
def get_all_stocks_repository() -> AllStocksPort:
    return SqliteAllStocksRepository(
        db_path=configs.db_path,
        db_table_name=configs.db_table_name
        )

def get_all_stocks_use_case(
    repo: AllStocksPort = Depends(get_all_stocks_repository)
    ) -> AllStocksUseCase:
    """
    Returns the use case for getting all stocks.
    """
    return AllStocksUseCase(stock_repository=repo)


# Delete stocks use case
def get_delete_stocks_repository() -> DeleteStocksPort:
    return SqliteDeleteStocksRepository(
        db_path=configs.db_path,
        db_table_name=configs.db_table_name
        )

def delete_stocks_use_case(
    repo: DeleteStocksPort = Depends(get_delete_stocks_repository)
    ) -> DeleteStocksUseCase:
    """
    Returns the use case for deleting all stocks.
    """
    return DeleteStocksUseCase(stock_repository=repo)