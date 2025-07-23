from fastapi.testclient import TestClient
from fastapi import status


def test_request_refund(client: TestClient):
    response = client.post(
        "/refunds/", json={}
    )

    data = response.json()

    assert response.status_code == status.HTTP_501_NOT_IMPLEMENTED
    assert data["detail"] == "Refunds not implemented yet"
