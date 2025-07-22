import uuid
from pydantic import BaseModel

class PaymentResponse(BaseModel):
    id: uuid.UUID
    createdAt: str
    status: str
    amount: int
    currency: str
    