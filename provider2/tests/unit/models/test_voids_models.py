import uuid
import pytest
from models.voids import Void
from pydantic import ValidationError


def test_void_model():
    void = Void(
        id=uuid.uuid4(),
        amount=50,
        transaction_id=uuid.uuid4()
    )
    assert isinstance(void.id, uuid.UUID)
    assert void.amount == 50
    assert isinstance(void.transaction_id, uuid.UUID)


def test_void_model_with_invalid_amount():
    with pytest.raises(ValidationError):
        void = Void(
            id=uuid.uuid4(),
            amount=-50,
            transaction_id=uuid.uuid4()
        )
        Void.model_validate(void)
