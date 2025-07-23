import pytest
import uuid
from fastapi.testclient import TestClient
from fastapi import status
from tests.conftest import check_db_connection


@pytest.mark.skipif(not check_db_connection(), reason="Requires database connection")
def test_void_request(client: TestClient):
    response = client.post(
        f"/void/{uuid.uuid4()}", json={
            "amount": 0
        }
    )

    data = response.json()

    assert response.status_code == status.HTTP_501_NOT_IMPLEMENTED
    assert data["detail"] == "Void operation is not implemented yet."


@pytest.mark.skipif(not check_db_connection(), reason="Requires database connection")
def test_void_request_wrong_payload(client: TestClient):
    response = client.post(
        f"/void/{uuid.uuid4()}", json={}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
