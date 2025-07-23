from pydantic import BaseModel, Field


class VoidRequest(BaseModel):
    amount: int = Field(..., ge=0, description="Amount must be a positive integer")
