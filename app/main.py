from fastapi import FastAPI

from app.routers import categories, expenses

app = FastAPI(title="Expense Tracker API", version="0.2.0")
app.include_router(categories.router)
app.include_router(expenses.router)


@app.get("/health")
def health():
    return {"status": "ok"}