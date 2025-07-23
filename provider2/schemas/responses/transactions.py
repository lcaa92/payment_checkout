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
