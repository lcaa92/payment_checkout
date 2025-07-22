import uuid
import datetime
from sqlmodel import Field, SQLModel

class CardDetails(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    number: str = Field(..., max_length=16)
    holder: str = Field(..., max_length=100)
    cvv: str = Field(..., max_length=4)
    expiration: str = Field(..., max_length=5)
    installmentNumber: int = Field(..., ge=1, le=12)

class PaymentType(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: str = Field(include=["card"], max_length=50) 
    card: uuid.UUID = Field(default=None, foreign_key="carddetails.id")

class Transaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    status: str = Field(include=["paid", "failed", "voided"])
    originalAmount: int = Field(..., ge=0)
    amount: int = Field(..., ge=0)
    currency: str = Field(..., max_length=3, include=["USD", "EUR", "BRL"]) 
    statementDescriptor: str = Field(..., max_length=255)
    paymenType: uuid.UUID = Field(default=None, foreign_key="paymenttype.id")

class Void(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date: str = Field(default_factory=datetime.datetime.now(datetime.timezone.utc))
    status: str = Field(include=["paid", "failed", "voided"])
    original_amount: int = Field(..., ge=0)
    amount: int = Field(..., ge=0)
    currency: str = Field(..., max_length=3, include=["USD", "EUR", "BRL"]) 
    statementDescriptor: str = Field(..., max_length=255)
    paymenType: str = Field(default=None, foreign_key="paymenttype.id")
