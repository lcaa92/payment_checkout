from fastapi import FastAPI

app = FastAPI()


@app.post("/transactions")
def transactions():
    # ToDo: Implement charge logic
    return {"Hello": "World"}


@app.get("/transactions/{id}")
def transaction_detail():
    # ToDo: Implement charge logic
    return {"Hello": "World"}


@app.post("/void/{id}")
def void(id: str):
    # ToDo: Implement refund logic
    return {"id": id}
