import uuid
import os
import datetime
import random
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends, HTTPException
from typing import Annotated
from form_input import ChargeRequest, RefundRequest
from models import Charge, CardDetails, PaymentMethod
from response import ChargeResponse, RefundResponse
from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.post("/charges", response_model=ChargeResponse, status_code=status.HTTP_201_CREATED)
def charges(input: ChargeRequest, session: SessionDep):

    charge = Charge(
        id=uuid.uuid4(),
        status=random.choice(["authorized", "refunded", "failed"]),  # Example status
        original_amount=input.amount,
        current_amount=input.amount,
        currency=input.currency,
        description=input.description,      
    )
    session.add(charge)
    session.commit()
    session.refresh(charge)

    payment_method = PaymentMethod(
        type=input.paymentMethod.type,
        charge_id=charge.id
    )

    session.add(payment_method)
    session.commit()
    session.refresh(payment_method)

    card_details = CardDetails(
        number=input.paymentMethod.card.number,
        holder_name=input.paymentMethod.card.holderName,
        cvv=input.paymentMethod.card.cvv,
        expiration_date=input.paymentMethod.card.expirationDate,
        installments=input.paymentMethod.card.installments,
        paymentmethod_id=payment_method.id
    )
    session.add(card_details)
    session.commit()
    session.refresh(card_details)

    return ChargeResponse(
        id=charge.id,
        createdAt=charge.created_at.isoformat(),
        status=charge.status,
        originalAmount=charge.original_amount, 
        currentAmount=charge.current_amount,
        currency=charge.currency,
        description=charge.description,
        paymentMethod=payment_method.type,
        cardId=card_details.id
    )

@app.get("/charges/{charge_id}", response_model=ChargeResponse)
def charges_detail(charge_id: str, session: SessionDep):
    charge = session.get(Charge, uuid.UUID(charge_id))
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    
    payment_method = session.exec(select(PaymentMethod).where(PaymentMethod.charge_id == charge.id)).first()
    card_details  = session.exec(select(CardDetails).where(CardDetails.paymentmethod_id == payment_method.id)).first()

    return ChargeResponse(
        id=charge.id,
        createdAt=charge.created_at.isoformat(),
        status=charge.status,
        originalAmount=charge.original_amount,
        currentAmount=charge.current_amount,
        currency=charge.currency,
        description=charge.description,
        paymentMethod=payment_method.type,
        cardId=card_details.id
    )


@app.post("/refund/{charge_id}", response_model=RefundRequest)
def refund(charge_id: str):
    # ToDo: Implement refund logic
    raise HTTPException(status_code=501, detail="Refund not implemented yet")
