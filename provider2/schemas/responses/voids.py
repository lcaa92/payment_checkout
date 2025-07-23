import uuid
from pydantic import BaseModel


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
