import logging
from typing import Union

from fastapi import APIRouter, Depends, Header

from app.auth.auth_bearer import JWTBearer
from app.config.settings import Settings, get_settings
from app.schemas.convert import ConversionData, ConversionResultResponse
from app.services.convert import currency_converter_service

router: APIRouter = APIRouter(prefix="/api/v1", dependencies=[Depends(JWTBearer())])


@router.post("/currency-converter", response_model=ConversionResultResponse)
async def currency_converter(
    conversion_data: ConversionData,
    settings: Settings = Depends(get_settings),
    authorization: Union[str, None] = Header(default=None)
) -> ConversionResultResponse:
    """
    Converts a given amount in the base currency to its equivalent in the target currency.

    Args:
    * from_currency (str): base currency
    * to_currency (str): target currency
    * amount (float): amount to be converted
    * settings (Settings): houses env vars and external URLs
    """
    authorization_token: str = authorization.split(' ')[1]

    # The service function does all the heavy lifting
    response = await currency_converter_service(
        conversion_data.from_currency,
        conversion_data.to_currency,
        conversion_data.amount,
        settings,
        auth_token=authorization_token
    )

    return response
