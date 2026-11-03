from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    category: str = Field(min_length=1, max_length=100)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    description: str | None = Field(default=None, max_length=255)
    spent_on: date


class Expense(ExpenseCreate):
    id: int