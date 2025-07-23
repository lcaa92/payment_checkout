import uuid
import pytest
from models.payments import Payments, PaymentStatus
from pydantic import ValidationError


def test_payments_model():
    payment = Payments(
        provider_id="123e4567-e89b-12d3-a456-426614174000",
        amount=100.0,
        currency="USD",
        status=PaymentStatus.pending
    )

    assert payment.provider_id == "123e4567-e89b-12d3-a456-426614174000"
    assert payment.amount == 100.0
    assert payment.currency == "USD"
    assert payment.status == PaymentStatus.pending
    assert isinstance(payment.id, uuid.UUID)


def test_payments_model_with_invalid_currency():
    with pytest.raises(ValidationError):
        payment = Payments(
            provider_id="123e4567-e89b-12d3-a456-426614174000",
            amount=100.0,
            currency="INVALID_CURRENCY",
            status=PaymentStatus.pending
        )
        Payments.model_validate(payment)
