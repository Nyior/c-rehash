from pydantic import BaseModel, Field


class HistoricalData(BaseModel):
    from_currency: str
    to_currency: str
    date: str = Field(description="Format: year-month-day: 2020-01-20")

    class Config:
        schema_extra = {
            "example": {
                "from_currency": "EUR",
                "to_currency": "NGN",
                "date": "2020-01-20",
            }
        }


class HistoricalDataResponse(BaseModel):
    from_currency: str
    to_currency: str
    exchange_date: str
    rate_at_date: float
