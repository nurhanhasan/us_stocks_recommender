from dataclasses import dataclass, field
from typing import List


@dataclass
class Stock:
    ticker: str
    company: str
    country: str
    sector: str
    industry: str
    shares_float: str
    short_interest: str
    relative_volume: str
    volume: str
    price: str
    change: str
    news_time: str
    news_title: str


@dataclass
class ScreenerResult:
    added: List[Stock] = field(default_factory=list)
    updated: List[Stock] = field(default_factory=list)
    unchanged: List[Stock] = field(default_factory=list)

    def __getitem__(self, key: str):
        return getattr(self, key)


@dataclass
class AllStocks:
    stocks: List[Stock] = field(default_factory=list)

    def __getitem__(self, key: str):
        return getattr(self, key)
