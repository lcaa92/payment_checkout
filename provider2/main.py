import uuid
import os
from typing import Annotated
from fastapi import FastAPI, status, Depends, HTTPException
from form_input import TransactionRequest, VoidRequest
from models import Transaction, TransactionStatus, CardDetails
from responses import TransactionResponse, VoidResponse
from sqlmodel import create_engine, Session, select
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def transactions(input: TransactionRequest, session: SessionDep):

    transaction = Transaction(
        id=uuid.uuid4(),
        status=TransactionStatus.get_random_status(),
        # status='paid',
        original_amount=input.amount,
        amount=input.amount,
        currency=input.currency,
        statement_descriptor=input.statementDescriptor,
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    card_details = CardDetails(
        number=input.card.number,
        holder=input.card.holder,
        cvv=input.card.cvv,
        expiration=input.card.expiration,
        installment_number=input.card.installmentNumber,
        transaction_id=transaction.id
    )
    session.add(card_details)
    session.commit()
    session.refresh(card_details)

    return TransactionResponse(
        id=transaction.id,
        date=transaction.created_at.isoformat(),
        status=transaction.status,
        originalAmount=transaction.original_amount,
        amount=transaction.amount,
        currency=transaction.currency,
        statementDescriptor=transaction.statement_descriptor,
        cardId=card_details.id
    )


@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def transaction_detail(transaction_id: str, session: SessionDep):
    transaction = session.get(Transaction, uuid.UUID(transaction_id))
    if not transaction_id:
        raise HTTPException(status_code=404, detail="Transaction not found")

    card_details = session.exec(select(CardDetails).where(CardDetails.transaction_id == transaction.id)).first()
    return TransactionResponse(
        id=transaction.id,
        date=transaction.created_at.isoformat(),
        status=transaction.status,
        originalAmount=transaction.original_amount,
        amount=transaction.amount,
        currency=transaction.currency,
        statementDescriptor=transaction.statement_descriptor,
        cardId=card_details.id
    )


@app.post("/void/{transaction_id}", response_model=VoidResponse)
def void(transaction_id: str, input: VoidRequest, session: SessionDep):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Void operation is not implemented yet."
    )
