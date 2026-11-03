from datetime import date
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.expense import Expense, ExpenseCreate

router = APIRouter(prefix="/expenses", tags=["expenses"])

# privremena "baza" u memoriji (tjedan 4 je zamjenjuje PostgreSQL-om)
_expenses: dict[int, Expense] = {}
_next_id = 1


@router.post("", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(data: ExpenseCreate):
    global _next_id
    expense = Expense(id=_next_id, **data.model_dump())
    _expenses[_next_id] = expense
    _next_id += 1
    return expense


@router.get("", response_model=list[Expense])
def list_expenses(
    category: str | None = None,
    min_amount: Decimal | None = Query(default=None, gt=0),
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    result = list(_expenses.values())
    if category:
        result = [e for e in result if e.category.lower() == category.lower()]
    if min_amount is not None:
        result = [e for e in result if e.amount >= min_amount]
    if date_from:
        result = [e for e in result if e.spent_on >= date_from]
    if date_to:
        result = [e for e in result if e.spent_on <= date_to]
    return result[offset : offset + limit]


@router.get("/{expense_id}", response_model=Expense)
def get_expense(expense_id: int):
    expense = _expenses.get(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, data: ExpenseCreate):
    if expense_id not in _expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense = Expense(id=expense_id, **data.model_dump())
    _expenses[expense_id] = expense
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    if _expenses.pop(expense_id, None) is None:
        raise HTTPException(status_code=404, detail="Expense not found")