import logging
import json
from datetime import timedelta

from fastapi import HTTPException

from app.config.settings import Settings
from app.utils.api_service import currency_api_caller
from app.utils.validator import are_valid_currencies
from app.utils.rate_limiter import request_is_limited
from app.cache.redis import redis_cache


CACHE_KEYS = {
    "RATES": "rates:exchange_rates"
}


async def get_rates(url: str):
        rates: float = await currency_api_caller(url)
        return rates.get('rates')


async def currency_converter_service(
    from_currency: str, 
    to: str, amount: float, 
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
    * amount (float): amount to convert from base to target currency.
    * settings (Settings): houses env vars and external URLs

    Returns:
    * response (dict): contains the converted amount, amount, to and from currencies.
    """

    # Check if user has exceeded their rate limit
    if await request_is_limited(key=auth_token):
        message = "Request rates exceeded."
        logging.exception(message)
        raise HTTPException(status_code=429, detail=message)

    # Check if the base & target currencies passed are supported
    if not are_valid_currencies(from_currency, to):
        message = "Invalid base or target currency."
        logging.exception(message)
        raise HTTPException(status_code=442, detail=message)

    URL: str = settings.OPEN_API_RATES

    # Get rates from redis cache
    rates = await redis_cache.get_key(CACHE_KEYS["RATES"])

    if rates:
        rates = json.loads(rates.decode('utf-8'))
        logging.info("rates loaded from redis cache")
    else:   
        # Get exchange rate from external API
        rates: float = await get_rates(URL)
        await redis_cache.set_key(
            key=CACHE_KEYS["RATES"], 
            value=json.dumps(rates).encode('utf-8'), 
            expire=timedelta(seconds=10800)
        )
        logging.info('loading rates from external api-- rates saved to redis')
    
    # converted_amount: float = amount * float(conversion_rate)
    converted_amount: float = amount * float(rates[to]/rates[from_currency])
    
    response: dict = {
        "from_currency": from_currency,
        "to_currency": to,
        "amount": amount,
        "converted_amount": converted_amount,
    }
    return response
