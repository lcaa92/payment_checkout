import pytest
from integrations.provider1 import Provider1Integration
from unittest.mock import patch, MagicMock


@pytest.fixture
def provider1():
    return Provider1Integration()


def test_build_payment_request(provider1):
    payment_data = {
        "amount": 200,
        "currency": "EUR",
        "description": "Test payment",
        "paymentInfo": {
            "number": "5555555555554444",
            "holderName": "Jane Doe",
            "cvv": "321",
            "expiration": "11/2026",
            "installments": 2
        }
    }
    req = provider1._build_payment_request(payment_data)
    assert req["amount"] == 200
    assert req["currency"] == "EUR"
    assert req["description"] == "Test payment"
    assert req["paymentMethod"]["type"] == "card"
    assert req["paymentMethod"]["card"]["number"] == "5555555555554444"
    assert req["paymentMethod"]["card"]["holderName"] == "Jane Doe"
    assert req["paymentMethod"]["card"]["cvv"] == "321"
    assert req["paymentMethod"]["card"]["expirationDate"] == "11/2026"
    assert req["paymentMethod"]["card"]["installments"] == 2


def test_build_get_payment_reload(provider1):
    payment_data = {"provider_id": "xyz789"}
    req = provider1._build_get_payment_reload(payment_data)
    assert req == {"id": "xyz789"}


@patch("integrations.provider1.requests.post")
def test_process_payment_success(mock_post, provider1):
    payment_data = {
        "amount": 200,
        "currency": "EUR",
        "description": "Test",
        "paymentInfo": {
            "number": "5555",
            "holderName": "Jane",
            "cvv": "321",
            "expiration": "11/2026",
            "installments": 2
        }
    }
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"status": "authorized"}
    mock_post.return_value = mock_response
    result = provider1.process_payment(payment_data)
    assert result["status"] == "authorized"


@patch("integrations.provider1.requests.post")
def test_process_payment_failure(mock_post, provider1):
    payment_data = {
        "amount": 200,
        "currency": "EUR",
        "description": "Test",
        "paymentInfo": {
            "number": "5555",
            "holderName": "Jane",
            "cvv": "321",
            "expiration": "11/2026",
            "installments": 2
        }
    }
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "fail"}
    mock_post.return_value = mock_response
    with pytest.raises(Exception):
        provider1.process_payment(payment_data)


@patch("integrations.provider1.requests.get")
def test_get_payment_details_success(mock_get, provider1):
    payment_data = {"provider_id": "xyz789"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "authorized"}
    mock_get.return_value = mock_response
    result = provider1.get_payment_details(payment_data)
    assert result["status"] == "authorized"


@patch("integrations.provider1.requests.get")
def test_get_payment_details_failure(mock_get, provider1):
    payment_data = {"provider_id": "xyz789"}
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "not found"}
    mock_get.return_value = mock_response
    with pytest.raises(Exception):
        provider1.get_payment_details(payment_data)


def test_get_status_from_response(provider1):
    assert provider1.get_status_from_response({"status": "authorized"}) is not None
    assert provider1.get_status_from_response({"status": "failed"}) is not None
    assert provider1.get_status_from_response({"status": "refunded"}) is not None
    assert provider1.get_status_from_response({"status": "unknown"}) is None
