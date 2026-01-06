import json
from pprint import pprint

from app.adapters.outbound.pyfinviz.pyfinviz_adapter import ExtendedScreener
from app.infrastructure.configs.config import configs
from pyfinviz.screener import Screener

# Filtering params
options = [
    Screener.PriceOption.USD1_TO_USD20,
    Screener.RelativeVolumeOption.OVER_5,
    Screener.ChangeOption.UP_10_PERCENT,
    Screener.FloatOption.UNDER_20M,
]

if configs.news_date_today:
    options.append(ExtendedScreener.NewsOption.TODAY)


# Custom settings to include in the screener view
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


# Instantiate
screener = ExtendedScreener(
    filter_options=options,
    view_option=Screener.ViewOption.CUSTOM_WITH_FILTERS,
    order_by=ExtendedScreener.ExtendedOrderBy.LATEST_NEWS,
    custom_settings_options=custom_settings_options,
)

# Available methods:
# print(screener.main_url)  # scraped URL
# print(screener.soups)  # beautiful soup object per page {1: soup, 2: soup, ...}
# print(screener.data_frames)  # table information in a pd.DataFrame object per page {1: table_df, 2, table_df, ...}

# Extended methods
# screener.to_csv()
changes = screener.scan()
json_result = json.dumps(changes, default=str, indent=4)
pprint(json_result)

