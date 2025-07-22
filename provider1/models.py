import datetime
import uuid
from sqlmodel import Field, SQLModel


class CardDetails(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    number: str = Field(..., max_length=16)
    holder_name: str = Field(..., max_length=100)
    cvv: str = Field(..., max_length=4)
    expiration_date: str = Field(..., max_length=7)  # Format: MM/YYYY
    installments: int = Field(..., ge=1, le=12)  # 1 to 12 installments
    paymentmethod_id : uuid.UUID = Field(default=None, foreign_key="paymentmethod.id")

class PaymentMethod(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: str = Field(include=["card"], max_length=50) 
    charge_id: uuid.UUID = Field(default=None, foreign_key="charge.id")

class Charge(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    status: str = Field(include=["authorized", "refunded", "failed"])
    original_amount: int = Field(..., ge=0)
    current_amount: int = Field(..., ge=0)
    currency: str = Field(..., max_length=3) 
    description: str = Field(..., max_length=255)
