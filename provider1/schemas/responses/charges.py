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
