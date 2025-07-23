import uuid
import pytest
from models.charges import Charge
from pydantic import ValidationError


def test_charge_model():
    charge = Charge(
        id=uuid.uuid4(),
        status="authorized",
        original_amount=100.0,
        current_amount=100.0,
        currency="USD",
        description="Test charge"
    )

    assert isinstance(charge.id, uuid.UUID)
    assert charge.status == "authorized"
    assert charge.original_amount == 100.0
    assert charge.current_amount == 100.0
    assert charge.currency == "USD"


def test_payments_model_with_invalid_currency():
    with pytest.raises(ValidationError):
        charge = Charge(
            id=uuid.uuid4(),
            status="authorized",
            original_amount=100.0,
            current_amount=100.0,
            currency="INVALID",
            description="Test charge"
        )
        Charge.model_validate(charge)
