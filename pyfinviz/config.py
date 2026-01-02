from pydantic_settings import BaseSettings

class Configs(BaseSettings):
    news_date_today: bool = True

configs = Configs()