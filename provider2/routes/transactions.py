import uuid
from fastapi import APIRouter, status, HTTPException
from schemas.form_input.transactions import TransactionRequest
from schemas.responses.transactions import TransactionResponse
from models.transactions import Transaction, TransactionStatus, CardDetails
from core.database import SessionDep
from sqlmodel import select


router = APIRouter(
    tags=["Transactions"],
)


@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def transactions(input: TransactionRequest, session: SessionDep):

    transaction = Transaction(
        id=uuid.uuid4(),
        status=TransactionStatus.get_random_status(),
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
        date=transaction.created_at.strftime("%Y-%m-%d"),
        status=transaction.status,
        originalAmount=transaction.original_amount,
        amount=transaction.amount,
        currency=transaction.currency,
        statementDescriptor=transaction.statement_descriptor,
        cardId=card_details.id
    )


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def transaction_detail(transaction_id: str, session: SessionDep):
    transaction = session.get(Transaction, uuid.UUID(transaction_id))
    if not transaction_id:
        raise HTTPException(status_code=404, detail="Transaction not found")

    card_details = session.exec(select(CardDetails).where(CardDetails.transaction_id == transaction.id)).first()
    return TransactionResponse(
        id=transaction.id,
        date=transaction.created_at.strftime("%Y-%m-%d"),
        status=transaction.status,
        originalAmount=transaction.original_amount,
        amount=transaction.amount,
        currency=transaction.currency,
        statementDescriptor=transaction.statement_descriptor,
        cardId=card_details.id
    )
