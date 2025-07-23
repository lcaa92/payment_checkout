from fastapi import FastAPI
from routes import refunds, payments

app = FastAPI()

app.include_router(payments.router)
app.include_router(refunds.router)
