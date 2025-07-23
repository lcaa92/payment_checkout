from fastapi.testclient import TestClient
from fastapi import FastAPI
from main import app

client = TestClient(app)


def test_app_instance():
    assert app is not None
    assert isinstance(app, FastAPI)
    assert app.title == "Payment Checkout API - Provider 1"
    assert app.description == "API for processing payments and refunds"
    assert app.version == "0.1.0"
