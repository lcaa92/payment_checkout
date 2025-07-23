from fastapi import FastAPI
from routes import refunds, charges

app = FastAPI(
    title="Payment Checkout API - Provider 1",
    description="API for processing payments and refunds",
    version="0.1.0",
)

app.include_router(refunds.router)
app.include_router(charges.router)
