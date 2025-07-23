import uuid
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from tests.conftest import check_db_connection


@pytest.mark.skipif(not check_db_connection(), reason="Requires database connection")
def test_create_charge(client: TestClient):
    response = client.post(
        "/transactions/", json={
            "amount": 0,
            "currency": "USD",
            "statementDescriptor": "string",
            "paymentType": "card",
            "card": {
                "number": "1234567890123456",
                "holder": "Holder Name",
                "cvv": "719",
                "expiration": "10/36",
                "installmentNumber": 1
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
        "/transactions/", json={
            "amount": 0,
            "currency": "USD",
            "statementDescriptor": "string",
            "paymentType": "string",
            "card": {
                "number": "123456789ddd0123456",
                "holder": "Holder Name",
                "cvv": "719",
                "expiration": "10/36",
                "installmentNumber": 1
            }
        }
    )

    data = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert data["detail"][0]["msg"] == "Input should be 'card'"
