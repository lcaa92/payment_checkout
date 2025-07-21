import uuid
from fastapi import FastAPI
from form_input import TransactionRequest, VoidRequest
from models import TransactionResponse, VoidResponse

app = FastAPI()


@app.post("/transactions", response_model=TransactionResponse)
def transactions(input: TransactionRequest):
    # ToDo: Implement charge logic
    return TransactionResponse(
        id=uuid.uuid4(),
        createdAt="2023-10-01T12:00:00Z",
        status="authorized",
        originalAmount=input.amount,
        currentAmount=input.amount,
        currency=input.currency,
        description=input.statementDescriptor,
        paymentMethod=input.paymentType.type,
        cardId=uuid.uuid4()  # Placeholder for card ID
    )


@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def transaction_detail(transaction_id: str):
    # ToDo: Implement charge logic
    return TransactionResponse(
        id=uuid.uuid4(),
        createdAt="2023-10-01T12:00:00Z",
        status="authorized",
        originalAmount=1000,
        currentAmount=1000,
        currency="USD",
        description="Sample Transaction",
        paymentMethod="card",
        cardId=uuid.uuid4()  # Placeholder for card ID
    )


@app.post("/void/{transaction_id}", response_model=VoidResponse)
def void(transaction_id: str, input: VoidRequest):
    # ToDo: Implement refund logic
    return VoidResponse(
        id=uuid.uuid4(),
        date="2023-10-01T12:00:00Z",
        status="voided",
        original_amount=input.amount,
        amount=input.amount,
        currency="USD", # Placeholder for currency  
        statementDescriptor="Sample Void",
        payment_type="card",  # Placeholder for payment type
        card_id=uuid.uuid4()  # Placeholder for card ID
    )
