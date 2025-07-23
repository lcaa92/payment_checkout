from fastapi import FastAPI
from routes import refunds, charges

app = FastAPI()

app.include_router(refunds.router)
app.include_router(charges.router)
