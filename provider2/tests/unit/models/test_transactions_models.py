import uuid
import pytest
from models.transactions import Transaction
from pydantic import ValidationError


def test_transaction_model():
    transaction = Transaction(
        id=uuid.uuid4(),
        status="paid",
        original_amount=100.0,
        amount=100.0,
        currency="USD",
        statement_descriptor="Test Transaction"
    )
    assert isinstance(transaction.id, uuid.UUID)
    assert transaction.status == "paid"
    assert transaction.original_amount == 100.0
    assert transaction.amount == 100.0


def test_transactions_model_with_invalid_currency():
    with pytest.raises(ValidationError):
        transaction = Transaction(
            id=uuid.uuid4(),
            status="paid",
            original_amount=100.0,
            amount=100.0,
            currency="INVALID",
            statement_descriptor="Test Transaction"
        )
        Transaction.model_validate(transaction)
