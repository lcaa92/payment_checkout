import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, status, HTTPException
from form_input import PaymentRequest
from responses import PaymentResponse
from models.payments import Payments, PaymentStatus
from services import paymentSrv
from core.database import SessionDep

load_dotenv()

app = FastAPI()


@app.post("/payments", response_model=PaymentResponse)
def payment(input: PaymentRequest, session: SessionDep):
    payment = Payments(
        provider_id=uuid.uuid4(),
        amount=input.amount,
        currency=input.currency,
        status=PaymentStatus.pending,
    )
    session.add(payment)
    session.commit()
    session.refresh(payment)

    paymentSrv.process_payment(
        input.model_dump(),
        payment,
        session
    )

    return PaymentResponse(
        id=payment.id,
        createdAt=payment.created_at.isoformat(),
        status=payment.status.value,
        amount=payment.amount,
        currency=payment.currency.value
    )


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def payment_detail(payment_id: uuid.UUID, session: SessionDep):
    payment = session.get(Payments, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    return PaymentResponse(
        id=payment.id,
        createdAt=payment.created_at.isoformat(),
        status=payment.status.value,
        amount=payment.amount,
        currency=payment.currency.value
    )


@app.post("/refunds")
def refunds():
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Refunds not implemented yet")
