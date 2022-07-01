import logging

from fastapi import HTTPException

from app.config.settings import Settings
from app.utils.api_service import currency_api_caller
from app.utils.validator import are_valid_currencies, is_valid_date


async def historical_data_service(
    from_currency: str, to: str, date: str, settings: Settings
):
    """
    Service for use in the currency_converter route handler.
    Houses all the currency conversion logic.

    Service functions foster Single Responsibility and Reusability.

    Args:
    * from_currency (str): base currency code
    * to (str): target currency code
    * date (str): date.
    * settings (Settings): houses env vars and external URLs

    Returns:
    * response (dict): contains the historical data
    """

    # Check if the base & target currencies passed are supported
    if not are_valid_currencies(from_currency, to):
        message = "Invalid base or target currency."
        logging.exception(message)
        raise HTTPException(status_code=442, detail=message)

    # Check if the passed date is valid
    if not is_valid_date(date):
        message = "Date has to be in this format: YYYY-MM-DD." f" Got {date}"

        logging.exception(message)
        raise HTTPException(status_code=442, detail=message)

    URL = settings.HISTORICAL_URL.format(date)
    query_params = {"from": from_currency, "to": to}

    # Get historical data from external API
    data = await currency_api_caller(settings, URL, query_params)
    rate = data["rates"][to]["rate"]

    response = {
        "from_currency": from_currency,
        "to_currency": to,
        "exchange_date": date,
        "rate_at_date": rate,
    }
    return response
