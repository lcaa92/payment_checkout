import uuid
from fastapi.testclient import TestClient


def test_create_transaction(client: TestClient):
    response = client.post(
        "/payments/", json={
            "amount": 0,
            "currency": "BRL",
            "description": "string",
            "paymentInfo": {
                "paymentType": "card",
                "number": "1234567890123456",
                "holderName": "Holder Name",
                "cvv": "315",
                "expiration": "03/2035",
                "installments": 1
            }
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data["id"], str)
    assert isinstance(uuid.UUID(data["id"]), uuid.UUID)


def test_create_transaction_wrong_payment_type(client: TestClient):
    response = client.post(
        "/payments/", json={
            "amount": 0,
            "currency": "BRL",
            "description": "string",
            "paymentInfo": {
                "paymentType": "pix",
                "number": "1234567890123456",
                "holderName": "Holder Name",
                "cvv": "315",
                "expiration": "03/2035",
                "installments": 1
            }
        }
    )

    data = response.json()

    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "Input should be 'card'"
