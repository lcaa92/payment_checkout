import uuid
from pydantic import BaseModel


class ChargeResponse(BaseModel):
    id: uuid.UUID
    createdAt: str
    status: str
    originalAmount: int
    currentAmount: int
    currency: str
    description: str
    paymentMethod: str
    cardId: uuid.UUID


class RefundResponse(BaseModel):
    id: uuid.UUID
    created_at: str
    status: str
    original_amount: int
    current_amount: int
    currency: str
    description: str
    payment_method: str
    card_id: uuid.UUID
