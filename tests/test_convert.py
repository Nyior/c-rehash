from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

BASE_URL = "/api/v1"


def test_currency_converter_with_valid_input():
    response = client.get(
        f"{BASE_URL}/currency-converter?from_currency=EUR&to_currency=NGN&amount=100"
    )
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "from_currency" in data and data["from_currency"] == "EUR"
    assert "to_currency" in data and data["to_currency"] == "NGN"
    assert "amount" in data and data["amount"] == 100
    assert "converted_amount" in data
    assert data["converted_amount"] > 0


def test_currency_converter_with_invalid_from_parameter():
    response = client.get(
        f"{BASE_URL}/currency-converter?from_currency=EURSS&to_currency=NGN&amount=100"
    )
    data = response.json()

    # EURSS is not defined in the SupportedCurrencies enum
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "converted_amount" not in data


def test_supported_currencies_returns_data():
    response = client.get(f"{BASE_URL}/supported-currencies")
    data = response.json()

    assert len(data) > 0
