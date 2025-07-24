import json
from integrations.orchestrator import PaymentOrchestrator, PaymentProcessException
from models.payments import Payments, PaymentStatus
from sqlmodel import Session


def process_payment(payment_data: dict, payment: Payments, session: Session) -> dict:
    """
    Process a payment request and store it in the database.
    """
    orchestrator = PaymentOrchestrator()

    try:
        data = orchestrator.process_payment(payment_data)
        payment.status = data.get("status")
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


def get_payment_details(payment: Payments) -> dict:
    """
    Process a payment request and store it in the database.
    """
    orchestrator = PaymentOrchestrator()
    return orchestrator.get_payment_details(payment)
