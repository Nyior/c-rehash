import logging
import json

from fastapi import HTTPException

from app.config.settings import Settings
from app.utils.api_service import currency_api_caller
from app.utils.rate_limiter import request_is_limited
from app.utils.validator import are_valid_currencies, is_valid_date
from app.cache.redis import redis_cache


CACHE_KEYS = {
    "HISTORICAL_RATES": "rates:historical_rates_{date}"
}

async def historical_data_service(
    from_currency: str, 
    to: str, 
    date: str, 
    settings: Settings, 
    auth_token: str
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
    async def get_historical_rates(url: str):
        rates: float = await currency_api_caller(url)
        return rates.get("rates")

    # Check if user has exceeded their rate limit
    if await request_is_limited(key=auth_token):
        message = "Request rates exceeded."
        logging.exception(message)
        raise HTTPException(status_code=429, detail=message)

    # Check if the base & target currencies passed are supported
    if not are_valid_currencies(from_currency, to):
        message = "base or target currency not supported."
        logging.exception(message)
        raise HTTPException(status_code=442, detail=message)

    # Check if the passed date is valid
    if not is_valid_date(date):
        message = f"Date has to be in this format: YYYY-MM-DD. Got {date}"
        logging.exception(message)
        raise HTTPException(status_code=442, detail=message)

    # URL = settings.HISTORICAL_URL.format(date)
    URL = settings.OPEN_API_HISTORICAL.format(date=date)

    rates = await redis_cache.get_key(
        CACHE_KEYS["HISTORICAL_RATES"].format(date=date)
    )

    if rates:
        rates = json.loads(rates.decode('utf-8'))
        print(f"HISTORICAL RATES: {rates}")
        logging.info("historical rates loaded from redis cache")
    else:   
        # Get exchange rate from external API
        rates: float = await get_historical_rates(URL)
        await redis_cache.set_key(
            key=CACHE_KEYS["HISTORICAL_RATES"].format(date=date), 
            value=json.dumps(rates).encode('utf-8'), 
            expire=10800
        )
        logging.info('loading rates from external api-- rates saved to redis')
   
    rate = rates[to]/rates[from_currency]

    response = {
        "from_currency": from_currency,
        "to_currency": to,
        "exchange_date": date,
        "rate_at_date": rate,
    }
    return response
