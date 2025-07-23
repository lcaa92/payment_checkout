from dotenv import load_dotenv
from fastapi import FastAPI
from routes import refunds, payments

load_dotenv()

app = FastAPI()

app.include_router(payments.router)
app.include_router(refunds.router)
