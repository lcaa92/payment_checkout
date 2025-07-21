from fastapi import FastAPI

app = FastAPI()


@app.post("/payments")
def payment():
    return {"Hello": "World"}


@app.get("/payments/{payment_id}")
def payment_detail(payment_id: str):
    return {"payment_id": payment_id}


@app.post("/refunds")
def refunds():
    return {"Hello": "World"}
