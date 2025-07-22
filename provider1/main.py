import uuid
import datetime
import random
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends, HTTPException
from typing import Annotated
from form_input import ChargeRequest, RefundRequest
from models import Charge, CardDetails, PaymentMethod
from response import ChargeResponse, RefundResponse
from sqlmodel import SQLModel, create_engine, Session
# app = FastAPI()


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

@app.post("/charges", response_model=ChargeResponse, status_code=status.HTTP_201_CREATED)
def charges(input: ChargeRequest, session: SessionDep):

    card_details = CardDetails(
        number=input.paymentMethod.card.number,
        holderName=input.paymentMethod.card.holderName,
        cvv=input.paymentMethod.card.cvv,
        expirationDate=input.paymentMethod.card.expirationDate,
        installments=input.paymentMethod.card.installments
    )
    session.add(card_details)  # Save card details
    session.commit()  # Commit the transaction to save the card details
    session.refresh(card_details)  # Refresh to get the ID of the saved card    

    payment_method = PaymentMethod(
        type=input.paymentMethod.type,
        card=card_details.id  # Assuming card ID is stored in the card model
    )

    session.add(payment_method)  # Save payment method
    session.commit()  # Commit the transaction to save the payment method
    session.refresh(payment_method)

    
    # Save charge details
    charge = Charge(
        id=uuid.uuid4(),
        createdAt=datetime.datetime.now(datetime.timezone.utc),
        status=random.choice(["authorized", "refunded", "failed"]),  # Example status
        originalAmount=input.amount,
        currentAmount=input.amount,
        currency=input.currency,
        description=input.description,      
        paymentMethod=payment_method.id,
        # cardId=payment_method.card  # Assuming card ID is stored in the card model
    )
    session.add(charge)
    session.commit()  # Commit the transaction to save the charge
    session.refresh(charge)  # Refresh to get the ID of the saved charge    

    return ChargeResponse(
        id=charge.id,
        createdAt=charge.createdAt.isoformat(),
        status=charge.status,
        originalAmount=charge.originalAmount, 
        currentAmount=charge.currentAmount,
        currency=charge.currency,
        description=charge.description,
        paymentMethod=input.paymentMethod.type,
        cardId=card_details.id
    )

@app.get("/charges/{charge_id}", response_model=ChargeResponse)
def charges_detail(charge_id: str, session: SessionDep):
    charge = session.get(Charge, uuid.UUID(charge_id))
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    
    payment_method = session.get(PaymentMethod, charge.paymentMethod)
    card_details = session.get(CardDetails, payment_method.card)
    return ChargeResponse(
        id=charge.id,
        createdAt=charge.createdAt.isoformat(),
        status=charge.status,
        originalAmount=charge.originalAmount,
        currentAmount=charge.currentAmount,
        currency=charge.currency,
        description=charge.description,
        paymentMethod=payment_method.type,
        cardId=card_details.id
    )


@app.post("/refund/{charge_id}", response_model=RefundRequest)
def refund(charge_id: str):
    # ToDo: Implement refund logic
    raise HTTPException(status_code=501, detail="Refund not implemented yet")
