import uuid
import datetime
from enum import Enum
from sqlmodel import Field, SQLModel

class PaymentMethodCurrency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    BRL = "BRL"


class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class Payments(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider: str = Field(..., include=['provider1', 'provider2'], description="Payment provider name")
    amount: int = Field(..., ge=0, description="Amount in cents")
    status: PaymentStatus = Field(default=PaymentStatus.pending.value, description="Current status of the payment")
    currency: PaymentMethodCurrency = Field(..., description="Currency must be a 3-letter ISO code")
    provider_id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier for the payment in the provider's system", alias="providerId")
    provider_details: str = Field(nullable=True, description="Details specific to the payment provider")
    created_at: str = Field(..., default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), description="Creation date in ISO 8601 format", alias="createdAt")
    