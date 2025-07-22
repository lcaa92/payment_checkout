from pydantic import BaseModel
from pydantic import BaseModel, Field
from models import PaymentMethodCurrency

class CardDetails(BaseModel):
    number: str = Field(..., min_length=16, max_length=16, description="Card number must be 16 digits")
    holder: str = Field(..., max_length=100, description="Holder must be up to 100 characters")
    cvv: str = Field(pattern=r"^\d{3}$", description="CVV must be 3 or 4 digits")
    expiration: str = Field(..., pattern=r"^(0[1-9]|1[0-2])/\d{2}$", description="Expiration date must be in MM/YY format")
    installmentNumber: int = Field(..., ge=1, le=12, description="installmentNumber must be between 1 and 12")

class TransactionRequest(BaseModel):
    amount: int = Field(..., ge=0, description="Amount must be a positive integer")
    currency: PaymentMethodCurrency = Field(..., max_length=3, description="Currency must be a 3-letter ISO code")
    statementDescriptor: str = Field(..., max_length=255)
    paymentType: str = Field(..., include=["card"], description="Payment type must be 'card' with card details")
    card: CardDetails = Field(..., description="Card details for the payment method") 
    
class VoidRequest(BaseModel):
    amount: int = Field(..., ge=0, description="Amount must be a positive integer")