import pytest
from fastapi.testclient import TestClient
from fastapi import status
from tests.conftest import check_db_connection


@pytest.mark.skipif(not check_db_connection(), reason="Requires database connection")
def test_request_refund(client: TestClient):
    response = client.post(
        "/refunds/", json={}
    )

    data = response.json()

    assert response.status_code == status.HTTP_501_NOT_IMPLEMENTED
    assert data["detail"] == "Refunds not implemented yet"
