from fastapi import FastAPI

from app.routers import expenses

app = FastAPI(title="Expense Tracker API", version="0.1.0")
app.include_router(expenses.router)


@app.get("/health")
def health():
    return {"status": "ok"}