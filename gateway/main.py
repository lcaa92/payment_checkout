from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes import refunds, payments

app = FastAPI(
    title='API Pay'
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "errors": {'.'.join(x['loc']): x['msg'] for x in exc.errors()},
        }),
    )


app.include_router(payments.router)
app.include_router(refunds.router)
