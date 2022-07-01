from enum import Enum


class SupportedCurrencies(str, Enum):
    """
    Predefined list of the currencies supported.
    """

    NGN = "NGN"
    USD = "USD"
    EUR = "EUR"
    BRL = "BRL"
    HKD = "HKD"
    ZAR = "ZAR"
    GHS = "GHS"
