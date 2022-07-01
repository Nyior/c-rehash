from app.enums.supported_currencies import SupportedCurrencies


def supported_currencies_service():
    """
    Service for use in the currencies route handler.

    Returns:
    * response (List): A list of currencies
    """
    return [currency.value for currency in SupportedCurrencies]
