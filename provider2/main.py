import uuid
import datetime
import random
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, status, Depends, HTTPException
from form_input import TransactionRequest, VoidRequest
from models import Transaction, Void, CardDetails, PaymentType
from responses import TransactionResponse, VoidResponse
from sqlmodel import SQLModel, create_engine, Session


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def transactions(input: TransactionRequest, session: SessionDep):
    card_details = CardDetails(
        number=input.paymentType.card.number,
        holder=input.paymentType.card.holder,
        cvv=input.paymentType.card.cvv,
        expiration=input.paymentType.card.expiration,
        installmentNumber=input.paymentType.card.installmentNumber
    )
    session.add(card_details)  # Save card details
    session.commit()  # Commit the transaction to save the card details
    session.refresh(card_details)  # Refresh to get the ID of the saved card    

    payment_type = PaymentType(
        type=input.paymentType.type,
        card=card_details.id  # Assuming card ID is stored in the card model
    )

    session.add(payment_type)  # Save payment method
    session.commit()  # Commit the transaction to save the payment method
    session.refresh(payment_type)

    
    # Save charge details
    transaction = Transaction(
        id=uuid.uuid4(),
        # date=datetime.datetime.now(datetime.timezone.utc),
        status=random.choice(["paid", "failed", "voided"]),
        originalAmount=input.amount,
        amount=input.amount,
        currency=input.currency,
        statementDescriptor=input.statementDescriptor,      
        paymenType=payment_type.id,
    )
    session.add(transaction)
    session.commit()  # Commit the transaction to save the charge
    session.refresh(transaction)  # Refresh to get the ID of the saved charge    

    return TransactionResponse(
        id=transaction.id,
        date=transaction.date.isoformat(),
        status=transaction.status,
        originalAmount=transaction.originalAmount, 
        amount=transaction.amount,
        currency=transaction.currency,
        statementDescriptor=transaction.statementDescriptor,
        paymentType=payment_type.type,
        cardId=card_details.id
    )


@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def transaction_detail(transaction_id: str, session: SessionDep):
    transaction = session.get(Transaction, uuid.UUID(transaction_id))
    if not transaction_id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    paymentType = session.get(PaymentType, transaction.paymenType)
    card_details = session.get(CardDetails, paymentType.card)
    return TransactionResponse(
        id=transaction.id,
        date=transaction.date.isoformat(),
        status=transaction.status,
        originalAmount=transaction.originalAmount, 
        amount=transaction.amount,
        currency=transaction.currency,
        statementDescriptor=transaction.statementDescriptor,
        paymentType=paymentType.type,
        cardId=card_details.id
    )

@app.post("/void/{transaction_id}", response_model=VoidResponse)
def void(transaction_id: str, input: VoidRequest, session: SessionDep):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Void operation is not implemented yet."
    )