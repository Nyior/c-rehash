import logging

from fastapi import HTTPException

from app.config.settings import Settings
from app.utils.api_service import currency_api_caller
from app.utils.validator import are_valid_currencies


async def currency_converter_service(
    from_currency: str, to: str, amount: float, settings: Settings
):
    """
    Service for use in the currency_converter route handler.
    Houses all the currency conversion logic.

    Service functions foster Single Responsibility and Reusability.

    Args:
    * from_currency (str): base currency code
    * to (str): target currency code
    * amount (float): amount to convert from base to target currency.
    * settings (Settings): houses env vars and external URLs

    Returns:
    * response (dict): contains the converted amount, amount, to and from currencies.
    """

    # Check if the base & target currencies passed are supported
    if not are_valid_currencies(from_currency, to):
        message = "Invalid base or target currency."
        logging.exception(message)
        raise HTTPException(status_code=442, detail=message)

    URL: str = settings.EXCHANGE_URL
    query_params: dict = {"from": from_currency, "to": to}

    # Get exchange rate for external API
    conversion_rate: float = await currency_api_caller(settings, URL, query_params)
    converted_amount: float = amount * float(conversion_rate)

    response: dict = {
        "from_currency": from_currency,
        "to_currency": to,
        "amount": amount,
        "converted_amount": converted_amount,
    }
    return response
