from fastapi import FastAPI
from routes import transactions, voids

app = FastAPI(
    title="Payment Checkout API Provider 2",
    description="API for processing payments and voids",
    version="0.1.0"
)

app.include_router(transactions.router)
app.include_router(voids.router)
