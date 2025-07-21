import datetime
import uuid
from sqlmodel import Field, SQLModel


class CardDetails(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    number: str = Field(..., max_length=16)
    holderName: str = Field(..., max_length=100)
    cvv: str = Field(..., max_length=4)
    expirationDate: str = Field(..., max_length=7)  # Format: MM/YYYY
    installments: int = Field(..., ge=1, le=12)  # 1 to 12 installments

class PaymentMethod(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid, primary_key=True)
    type: str = Field(include=["card"], max_length=50) 
    card: int = Field(default=None, foreign_key="carddetails.id")

class Charge(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    createdAt: datetime.datetime = Field(default_factory=datetime.datetime.now(datetime.timezone.utc))
    status: str = Field(include=["authorized", "refunded", "failed"])
    originalAmount: int = Field(..., ge=0)
    currentAmount: int = Field(..., ge=0)
    currency: str = Field(..., max_length=3) 
    description: str = Field(..., max_length=255)
    paymentMethod: int = Field(default=None, foreign_key="paymentmethod.id")

# class ChargeResponse(BaseModel):
#     id: uuid.UUID
#     createdAt: str
#     status: str
#     originalAmount: int
#     currentAmount: int
#     currency: str 
#     description: str
#     paymentMethod: str 
#     cardId: uuid.UUID
    

# class RefundResponse(BaseModel):
#     id: uuid.UUID
#     created_at: str
#     status: str
#     original_amount: int
#     current_amount: int
#     currency: str
#     description: str
#     payment_method: str
#     card_id: uuid.UUID
