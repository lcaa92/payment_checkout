from enum import Enum
from pydantic import BaseModel, Field, field_validator


class CardDetails(BaseModel):
    number: str = Field(..., min_length=16, max_length=16, description="Card number must be 16 digits")
    holderName: str = Field(..., max_length=100, description="Holder name must be up to 100 characters")
    cvv: str = Field(pattern=r"^[0-9]{3, 4}$", description="CVV must be 3 or 4 digits")
    expirationDate: str = Field(
        ...,
        pattern=r"^(0[1-9]|1[0-2])/\d{4}$",
        description="Expiration date must be in MM/YYYY format"
    )
    installments: int = Field(..., ge=1, le=12, description="Installments must be between 1 and 12")

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

    @field_validator("expirationDate", mode="before")
    @classmethod
    def validate_expiration_date(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("Expiration date must be a non-empty string in MM/YYYY format")
        parts = v.split('/')
        if len(parts) != 2 or not (parts[0].isdigit() and parts[1].isdigit()):
            raise ValueError("Expiration date must be in MM/YYYY format")
        return v


class PaymentMethodType(str, Enum):
    CARD = "card"


class PaymentMethod(BaseModel):
    type: PaymentMethodType = Field(..., description="Payment method type must be 'card'")
    card: CardDetails = Field(..., description="Card details for the payment method")


class PaymentMethodCurrency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    BRL = "BRL"


class ChargeRequest(BaseModel):
    amount: int = Field(..., ge=0, description="Amount must be a positive integer")
    currency: PaymentMethodCurrency = Field(..., max_length=3, description="Currency must be a 3-letter ISO code")
    description: str = Field(..., max_length=255, description="Description must be up to 255 characters")
    paymentMethod:  PaymentMethod = Field(..., description="Payment method details")
