from fastapi import FastAPI

app = FastAPI()


@app.post("/charges")
def charges():
    # ToDo: Implement charge logic
    return {"Hello": "World"}


@app.get("/charges{id}")
def charges_detail():
    # ToDo: Implement charge logic
    return {"Hello": "World"}


@app.post("/refund/{id}")
def refund(id: str):
    # ToDo: Implement refund logic
    return {"id": id}
