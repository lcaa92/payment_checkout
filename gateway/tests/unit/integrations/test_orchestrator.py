import uuid
import pytest
from integrations.orchestrator import PaymentOrchestrator, PaymentProcessException


@pytest.fixture
def orchestrator():
    return PaymentOrchestrator()


def test_process_payment_success(monkeypatch):
    class DummyProvider:
        def process_payment(self, payment_data):
            return {"status": "authorized"}

        def get_status_from_response(self, data):
            return "completed"

    orchestrator = PaymentOrchestrator({"dummy": DummyProvider})
    payment_data = {"amount": 100, "currency": "USD", "paymentInfo": {}}
    result = orchestrator.process_payment(payment_data)
    assert result["provider_name"] == "dummy"
    assert result["status"] == "completed"


def test_process_payment_all_fail():
    class DummyProvider:
        def process_payment(self, payment_data):
            raise Exception("fail")

        def get_status_from_response(self, data):
            return "failed"

    orchestrator = PaymentOrchestrator({"dummy": DummyProvider})
    payment_data = {"amount": 100, "currency": "USD", "paymentInfo": {}}
    with pytest.raises(PaymentProcessException) as exc:
        orchestrator.process_payment(payment_data)

    assert "All payment providers failed" in str(exc.value)
    assert len(exc.value.errors) == 1


def test_get_payment_details_success():
    class DummyProvider:
        def get_payment_details(self, data):
            return {"status": "authorized"}

    class DummyPayment:
        id = uuid.uuid4()
        provider = "dummy"
        provider_id = uuid.uuid4()

        def model_dump(self):
            return {"provider_id": "abc123"}

    orchestrator = PaymentOrchestrator({"dummy": DummyProvider})
    payment = DummyPayment()
    result = orchestrator.get_payment_details(payment)
    assert result["status"] == "authorized"


def test_get_payment_details_unknown_provider():
    class DummyPayment:
        provider = "unknown"

        def model_dump(self):
            return {"provider_id": "abc123"}

    orchestrator = PaymentOrchestrator({"dummy": object})
    payment = DummyPayment()
    with pytest.raises(ValueError):
        orchestrator.get_payment_details(payment)
