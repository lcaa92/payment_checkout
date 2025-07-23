import uuid
from sqlmodel import Field, SQLModel


class Void(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: int = Field(..., ge=0)
    transaction_id: uuid.UUID = Field(default=None, foreign_key="transaction.id")
