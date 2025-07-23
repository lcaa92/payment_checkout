from fastapi import APIRouter, status, HTTPException

router = APIRouter(
    tags=["Refunds"],
)


@router.post("/refunds")
def refunds():
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Refunds not implemented yet")
