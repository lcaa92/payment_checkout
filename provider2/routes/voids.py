from fastapi import APIRouter, status, HTTPException
from schemas.form_input.voids import VoidRequest
from schemas.responses.voids import VoidResponse
from core.database import SessionDep

router = APIRouter(
    tags=["Voids"],
)


@router.post("/void/{transaction_id}", response_model=VoidResponse)
def void(transaction_id: str, input: VoidRequest, session: SessionDep):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Void operation is not implemented yet."
    )
