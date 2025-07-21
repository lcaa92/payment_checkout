import uuid
from pydantic import BaseModel

class PaymentMethod(BaseModel):
    type: str  # e.g., "card", "bank_transfer", etc.
    card: 'CardDetails' = None  # Optional, only if type is "card"

class CardDetails(BaseModel):
    number: str
    holderName: str
    cvv: str
    expirationDate: str
    installments: int

class ChargeRequest(BaseModel):
    amount: int
    currency: str
    description: str
    paymentMethod: PaymentMethod
    

class RefundRequest(BaseModel):
    amount: int