from pydantic import BaseModel, Field


class ConversionData(BaseModel):
    """Defines the structure of the data to be converted"""

    from_currency: str
    to_currency: str
    amount: float = Field(gt=0, description="The amount must be greater than zero")

    class Config:
        schema_extra = {
            "example": {"from_currency": "EUR", "to_currency": "NGN", "amount": 35.4}
        }


class ConversionResultResponse(BaseModel):
    """Defines the structure of the response returned after a conversion"""

    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
