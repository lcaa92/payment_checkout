import json
from integrations.orchestrator import PaymentOrchestrator, PaymentProcessException
from models import Payments, PaymentStatus
from sqlmodel import Session


def process_payment(payment_data: dict, payment: Payments, session: Session) -> dict:
    """
    Process a payment request and store it in the database.
    """
    orchestrator = PaymentOrchestrator()

    try:
        data = orchestrator.process_payment(payment_data)
        payment.status = PaymentStatus.completed
        payment.provider = data.get("provider_name")
        payment.provider_id = data.get("provider_details", {}).get("id")
        payment.provider_details = json.dumps(data.get("provider_details", {}))
    except PaymentProcessException as e:
        payment.status = PaymentStatus.failed
        payment.provider_details = str(e.errors)
    finally:
        session.add(payment)
        session.commit()
        session.refresh(payment)