import uuid
from fastapi import FastAPI
from form_input import ChargeRequest, RefundRequest
from models import ChargeResponse, RefundResponse
app = FastAPI()


@app.post("/charges", response_model=ChargeResponse)
def charges(input: ChargeRequest):
    # ToDo: Implement charge logic
    return ChargeResponse(
        id=uuid.uuid4(),
        createdAt="2023-10-01T12:00:00Z",
        status="authorized",
        originalAmount=input.amount,
        currentAmount=input.amount,
        currency=input.currency,
        description=input.description,
        paymentMethod=input.paymentMethod.type,
        cardId=uuid.uuid4() if input.paymentMethod.type == "card" else None
    )


@app.get("/charges/{charge_id}", response_model=ChargeResponse)
def charges_detail(charge_id: str, input: ChargeRequest):
    # ToDo: Implement charge logic
    return ChargeResponse(
        id=uuid.uuid4(),
        createdAt="2023-10-01T12:00:00Z",
        status="authorized",
        originalAmount=input.amount,
        currentAmount=input.amount,
        currency=input.currency,
        description=input.description,
        paymentMethod=input.paymentMethod.type,
        cardId=uuid.uuid4() if input.paymentMethod.type == "card" else None
    )


@app.post("/refund/{charge_id}", response_model=RefundRequest)
def refund(charge_id: str):
    # ToDo: Implement refund logic
    return RefundResponse(
        id=uuid.uuid4(),
        created_at="2023-10-01T12:00:00Z",
        status="refunded",
        original_amount=1000,  # Example amount
        current_amount=1000,  # Example amount
        currency="USD",  # Example currency
        description="Refund for charge",
        payment_method="card",  # Example payment method
        card_id=uuid.uuid4()  # Example card ID
    )
