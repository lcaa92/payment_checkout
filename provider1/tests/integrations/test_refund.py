import pytest
import uuid
from fastapi.testclient import TestClient
from fastapi import status
from tests.conftest import check_db_connection


@pytest.mark.skipif(not check_db_connection(), reason="Requires database connection")
def test_request_refund(client: TestClient):
    response = client.post(
        f"/refund/{uuid.uuid4()}", json={
            "amount": 0
        }
    )

    data = response.json()

    assert response.status_code == status.HTTP_501_NOT_IMPLEMENTED
    assert data["detail"] == "Refund not implemented yet"


@pytest.mark.skipif(not check_db_connection(), reason="Requires database connection")
def test_request_refund_wrong_payload(client: TestClient):
    response = client.post(
        f"/refund/{uuid.uuid4()}", json={}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
