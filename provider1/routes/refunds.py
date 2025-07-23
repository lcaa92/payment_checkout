import uuid
from fastapi import APIRouter, status, HTTPException
from schemas.form_input.charges import RefundRequest
from schemas.responses.refunds import RefundResponse

router = APIRouter(
    tags=["Refunds"],
)


@router.post("/refund/{charge_id}", response_model=RefundResponse)
def refund(charge_id: uuid.UUID, input: RefundRequest):
    # ToDo: Implement refund logic
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Refund not implemented yet")
