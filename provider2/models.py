import uuid
import datetime
import random
from enum import Enum
from sqlmodel import Field, SQLModel

class PaymentMethodCurrency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    BRL = "BRL"

class TransactionStatus(str, Enum):
    paid = "paid"
    failed = "failed"
    voided = "voided"

    @classmethod
    def get_random_status(cls):
        return random.choice(list(cls))

class CardDetails(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    number: str = Field(..., max_length=16)
    holder: str = Field(..., max_length=100)
    cvv: str = Field(..., max_length=4)
    expiration: str = Field(..., max_length=5)
    installment_number: int = Field(..., ge=1, le=12)
    transaction_id: uuid.UUID = Field(default=None, foreign_key="transaction.id")

class Transaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), alias="created_at")
    status: TransactionStatus = Field(description="Transaction status")
    original_amount: int = Field(..., ge=0)
    amount: int = Field(..., ge=0)
    currency: PaymentMethodCurrency = Field(..., max_length=3, description="Currency must be a 3-letter ISO code") 
    statement_descriptor: str = Field(..., max_length=255)

class Void(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: int = Field(..., ge=0)
    transaction_id: uuid.UUID = Field(default=None, foreign_key="transaction.id")
