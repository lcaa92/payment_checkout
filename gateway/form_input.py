from pydantic import BaseModel, Field
from models import PaymentMethodCurrency

class PaymentInfo(BaseModel):
    paymentType: str = Field(..., includes=["card"], description="Payment type must be 'card'")
    number: str = Field(..., min_length=16, max_length=16, description="Card number must be 16 digits")
    holderName: str = Field(..., max_length=100, description="Holder must be up to 100 characters")
    cvv: str = Field(pattern=r"^\d{3}$", description="CVV must be 3 or 4 digits")
    expiration: str = Field(..., pattern=r"^(0[1-9]|1[0-2])/\d{4}$", description="Expiration date must be in MM/YYYY format")
    installments: int = Field(..., ge=1, le=12, description="Number of installments must be between 1 and 12")

class PaymentRequest(BaseModel):
    amount: int
    currency: PaymentMethodCurrency = Field(..., max_length=3, description="Currency must be a 3-letter ISO code")
    description: str = Field(..., max_length=255, description="Description of the payment")
    paymentInfo: PaymentInfo = Field(..., description="Payment method details")
    