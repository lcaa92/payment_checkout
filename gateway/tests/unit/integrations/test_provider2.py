import pytest
from integrations.provider2 import Provider2Integration
# import requests
from unittest.mock import patch, MagicMock


@pytest.fixture
def provider2():
    return Provider2Integration()


def test_build_payment_request(provider2):
    payment_data = {
        "amount": 100,
        "currency": "USD",
        "description": "Test payment",
        "paymentInfo": {
            "number": "4111111111111111",
            "holderName": "John Doe",
            "cvv": "123",
            "expiration": "12/2025",
            "installments": 1
        }
    }
    req = provider2._build_payment_request(payment_data)
    assert req["amount"] == 100
    assert req["currency"] == "USD"
    assert req["card"]["number"] == "4111111111111111"
    assert req["card"]["holder"] == "John Doe"
    assert req["card"]["cvv"] == "123"
    assert req["card"]["expiration"] == "12/25"
    assert req["card"]["installmentNumber"] == 1


def test_build_get_payment_reload(provider2):
    payment_data = {"provider_id": "abc123"}
    req = provider2._build_get_payment_reload(payment_data)
    assert req == {"id": "abc123"}


@patch("integrations.provider2.requests.post")
def test_process_payment_success(mock_post, provider2):
    payment_data = {
        "amount": 100,
        "currency": "USD",
        "description": "Test",
        "paymentInfo": {
            "number": "4111",
            "holderName": "John",
            "cvv": "123",
            "expiration":
            "12/2025",
            "installments": 1
        }
    }
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"status": "paid"}
    mock_post.return_value = mock_response
    result = provider2.process_payment(payment_data)
    assert result["status"] == "paid"


@patch("integrations.provider2.requests.post")
def test_process_payment_failure(mock_post, provider2):
    payment_data = {
        "amount": 100,
        "currency": "USD",
        "description": "Test",
        "paymentInfo": {
            "number": "4111",
            "holderName": "John",
            "cvv": "123",
            "expiration": "12/2025",
            "installments": 1
        }
    }
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "fail"}
    mock_post.return_value = mock_response
    with pytest.raises(Exception):
        provider2.process_payment(payment_data)


@patch("integrations.provider2.requests.get")
def test_get_payment_details_success(mock_get, provider2):
    payment_data = {"provider_id": "abc123"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "paid"}
    mock_get.return_value = mock_response
    result = provider2.get_payment_details(payment_data)
    assert result["status"] == "paid"


@patch("integrations.provider2.requests.get")
def test_get_payment_details_failure(mock_get, provider2):
    payment_data = {"provider_id": "abc123"}
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "not found"}
    mock_get.return_value = mock_response
    with pytest.raises(Exception):
        provider2.get_payment_details(payment_data)


def test_get_status_from_response(provider2):
    assert provider2.get_status_from_response({"status": "paid"}) is not None
    assert provider2.get_status_from_response({"status": "failed"}) is not None
    assert provider2.get_status_from_response({"status": "voided"}) is not None
    assert provider2.get_status_from_response({"status": "unknown"}) is None
