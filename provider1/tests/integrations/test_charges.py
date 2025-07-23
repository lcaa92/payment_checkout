import uuid
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from tests.conftest import check_db_connection


@pytest.mark.skipif(not check_db_connection(), reason="Requires database connection")
def test_create_charge(client: TestClient):
    response = client.post(
        "/charges/", json={
            "amount": 0,
            "currency": "USD",
            "description": "string",
            "paymentMethod": {
                "type": "card",
                "card": {
                    "number": "1234567890123456",
                    "holderName": "string",
                    "cvv": "123",
                    "expirationDate": "12/7377",
                    "installments": 1
                }
            }
        }
    )

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(data["id"], str)
    assert isinstance(uuid.UUID(data["id"]), uuid.UUID)


@pytest.mark.skipif(not check_db_connection(), reason="Requires database connection")
def test_create_charges_wrong_payment_type(client: TestClient):
    response = client.post(
        "/charges/", json={
            "amount": 0,
            "currency": "USD",
            "description": "string",
            "paymentMethod": {
                "type": "pix",
                "card": {
                    "number": "1234567890123456",
                    "holderName": "string",
                    "cvv": "123",
                    "expirationDate": "12/7377",
                    "installments": 1
                }
            }
        }
    )

    data = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert data["detail"][0]["msg"] == "Input should be 'card'"
