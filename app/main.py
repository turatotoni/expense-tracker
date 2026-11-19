from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import ConflictError, InvalidInputError, NotFoundError, UnauthorizedError
from app.routers import auth, categories, expenses

app = FastAPI(title="Expense Tracker API", version="0.4.0")
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(InvalidInputError)
async def invalid_input_handler(request: Request, exc: InvalidInputError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/health")
def health():
    return {"status": "ok"}