from fastapi import FastAPI

from app.routers import auth, categories, expenses

app = FastAPI(title="Expense Tracker API", version="0.3.0")
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)


@app.get("/health")
def health():
    return {"status": "ok"}