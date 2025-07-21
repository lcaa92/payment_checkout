import uuid
from pydantic import BaseModel

class TransactionResponse(BaseModel):
    id: uuid.UUID
    createdAt: str
    status: str
    originalAmount: int
    currentAmount: int
    currency: str
    description: str
    paymentMethod: str
    cardId: uuid.UUID

class VoidResponse(BaseModel):
    id: uuid.UUID
    date: str
    status: str
    original_amount: int
    amount: int
    currency: str
    statementDescriptor: str
    payment_type: str
    card_id: uuid.UUID
