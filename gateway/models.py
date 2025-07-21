import uuid
from pydantic import BaseModel

class PaymentResponse(BaseModel):
    id: uuid.UUID
    createdAt: str  # ISO 8601 format date string
    status: str  # e.g., "authorized", "failed", "refunded"
    originalAmount: int
    currentAmount: int
    currency: str  # ISO 4217 format
    description: str
    paymentMethod: str  # e.g., "card"
    cardId: uuid.UUID
    