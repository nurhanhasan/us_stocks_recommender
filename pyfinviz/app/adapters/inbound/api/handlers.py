from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.models.entities import Stock
from app.application.services.stock_screener_use_cases import (
    AllStocksUseCase, DeleteStocksUseCase, ScreenerUseCase)
from app.infrastructure.dependencies import (delete_stocks_use_case,
                                             get_all_stocks_use_case,
                                             get_screen_stocks_use_case)


class ChangeSummaryResponse(BaseModel):
    added: List[dict]
    updated: List[dict]
    unchanged: List[dict]


class StockResponse(BaseModel):
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

    @staticmethod
    # convert stock to dict
    def to_dict(stock: Stock):
        return {
            "ticker": stock.ticker,
            "company": stock.company,
            "country": stock.country,
            "sector": stock.sector,
            "industry": stock.industry,
            "shares_float": stock.shares_float,
            "short_interest": stock.short_interest,
            "relative_volume": stock.relative_volume,
            "volume": stock.volume,
            "price": stock.price,
            "change": stock.change,
            "news_time": stock.news_time,
            "news_title": stock.news_title,
        }


class AllStocksResponse(BaseModel):
    stocks: List[dict]


router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/scan", response_model=ChangeSummaryResponse)
async def scan_stocks(
    use_case: ScreenerUseCase = Depends(get_screen_stocks_use_case),
) -> ChangeSummaryResponse:
    """
    Triggers the stock screener independently.
    This is a synchronous call that waits for the scraping to finish.
    """

    screener_resuts = use_case.execute()
    return ChangeSummaryResponse(
        added=[StockResponse.to_dict(stock) for stock in screener_resuts.added],
        updated=[StockResponse.to_dict(stock) for stock in screener_resuts.updated],
        unchanged=[StockResponse.to_dict(stock) for stock in screener_resuts.unchanged],
    )


@router.get("/stocks", response_model=AllStocksResponse)
async def get_stocks(
    use_case: AllStocksUseCase = Depends(get_all_stocks_use_case),
) -> AllStocksResponse:
    """
    Returns the list of stocks in the database.
    """
    stocks_data = use_case.execute()
    return AllStocksResponse(
        stocks=[StockResponse.to_dict(stock) for stock in stocks_data.stocks]
    )


@router.delete("/stocks")
async def delete_stocks(
    use_case: DeleteStocksUseCase = Depends(delete_stocks_use_case),
) -> dict:
    """
    Deletes all stocks from the database.
    """
    try:
        use_case.execute()
        return {"message": "Stocks deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
