import json

from config import configs
from pyfinviz_ext.screener import PersistableScreener as Screener
from pyfinviz_ext.screener import ScreenerWrapper


extended_screener = ScreenerWrapper()

# Filtering params
options = [
    Screener.PriceOption.USD1_TO_USD20,
    Screener.RelativeVolumeOption.OVER_5,
    Screener.ChangeOption.UP_10_PERCENT,
    Screener.FloatOption.UNDER_20M,
    # extended_screener.NewsOption.TODAY
]

if configs.news_date_today:
    options.append(extended_screener.NewsOption.TODAY)


# Custom settings to include in the screener view
custom_settings_options = [
    Screener.CustomSettingsOption.NO,
    Screener.CustomSettingsOption.TICKER,
    Screener.CustomSettingsOption.COMPANY,
    Screener.CustomSettingsOption.COUNTRY,
    Screener.CustomSettingsOption.SECTOR,
    Screener.CustomSettingsOption.SHARES_FLOAT,
    Screener.CustomSettingsOption.SHORT_INTEREST,
    Screener.CustomSettingsOption.RELATIVE_VOLUME,
    Screener.CustomSettingsOption.VOLUME,
    Screener.CustomSettingsOption.PRICE,
    Screener.CustomSettingsOption.CHANGE,
    extended_screener.ExtendedCustomSettingsOption.NEWS_TIME,
    extended_screener.ExtendedCustomSettingsOption.NEWS_TITLE,
]



# Instantiate
screener = Screener(
    filter_options=options,
    view_option=Screener.ViewOption.CUSTOM_WITH_FILTERS,
    order_by=extended_screener.ExtendedOrderBy.LATEST_NEWS,
    custom_settings_options=custom_settings_options,
)

# Available methods:
# print(screener.main_url)  # scraped URL
# print(screener.soups)  # beautiful soup object per page {1: soup, 2: soup, ...}
# print(screener.data_frames)  # table information in a pd.DataFrame object per page {1: table_df, 2, table_df, ...}

# Extended methods
# screener.to_csv()
changes = screener.to_updated_deduplicated_sqlite()
json_result = json.dumps(changes, default=str, indent=4)
print(json_result)

