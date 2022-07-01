from datetime import datetime

from app.services.supported_currencies import supported_currencies_service


def is_valid_currency(currency: str) -> bool:
    """
    Checks if a single currency is supported

    Args:
    * currency (str): currency code to be checked

    Returns:
        bool:
    """
    # Get list of supported currencies
    currency_codes = supported_currencies_service()

    # If the currency is not in the list, it's invalid
    if currency not in currency_codes:
        return False

    return True


def are_valid_currencies(from_currency: str, to_currency: str) -> str:
    """
    Checks if the base and target currencies are supported.

    Args:
    * from_currency (str): base currency code to be checked
    * to_currency (str): target currency code to be checked
    """
    if not is_valid_currency(from_currency) or not is_valid_currency(to_currency):
        return False

    return True


def is_valid_date(date: str) -> bool:
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        return False

    return True
