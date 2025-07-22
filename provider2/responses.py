import uuid
from pydantic import BaseModel


class TransactionResponse(BaseModel):
    id: uuid.UUID
    date: str
    status: str
    originalAmount: int
    amount: int
    currency: str
    statementDescriptor: str
    cardId: uuid.UUID


class VoidResponse(BaseModel):
    id: uuid.UUID
    created_at: str
    status: str
    original_amount: int
    current_amount: int
    currency: str
    description: str
    payment_method: str
    card_id: uuid.UUID
