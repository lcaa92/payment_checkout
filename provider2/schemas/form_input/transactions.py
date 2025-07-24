from enum import Enum
from pydantic import BaseModel, Field, field_validator
from models.transactions import PaymentMethodCurrency


class CardDetails(BaseModel):
    number: str = Field(..., pattern=r"^\d{16}$", description="Card number must be 16 digits")
    holder: str = Field(..., max_length=100, description="Holder must be up to 100 characters")
    cvv: str = Field(pattern=r"^\d{3}$", description="CVV must be 3 or 4 digits")
    expiration: str = Field(
        ...,
        pattern=r"^(0[1-9]|1[0-2])/\d{2}$",
        description="Expiration date must be in MM/YY format"
    )
    installmentNumber: int = Field(..., ge=1, le=12, description="installmentNumber must be between 1 and 12")

    @field_validator("number", mode="before")
    @classmethod
    def validate_card_number(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 16:
            raise ValueError("Card number must be a 16 digit number")
        return v

    @field_validator("cvv", mode="before")
    @classmethod
    def validate_cvv(cls, v: str) -> str:
        if not v.isdigit() or len(v) not in [3, 4]:
            raise ValueError("CVV must be a 3 or 4 digit number")
        return v


class PaymentType(str, Enum):
    card = "card"


class TransactionRequest(BaseModel):
    amount: int = Field(..., ge=0, description="Amount must be a positive integer")
    currency: PaymentMethodCurrency = Field(..., max_length=3, description="Currency must be a 3-letter ISO code")
    statementDescriptor: str = Field(..., max_length=255)
    paymentType: PaymentType = Field(..., description="Payment type must be 'card' with card details")
    card: CardDetails = Field(..., description="Card details for the payment method")
