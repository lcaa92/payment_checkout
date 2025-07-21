import uuid
from fastapi import FastAPI
from form_input import Payment  
from models import PaymentResponse 

app = FastAPI()


@app.post("/payments", response_model=PaymentResponse)
def payment(input: Payment):
    return PaymentResponse(
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


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def payment_detail(payment_id: str):
    return PaymentResponse(
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



@app.post("/refunds")
def refunds():
    return {"Hello": "World"}
