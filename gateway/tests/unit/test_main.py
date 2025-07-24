from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_app_instance():
    assert app is not None
    assert app.title == 'API Pay'
