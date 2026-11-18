from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_current_user_id, get_expense_service
from app.schemas.expense import Expense, ExpenseCreate
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(
    data: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
    user_id: int = Depends(get_current_user_id),
):
    return service.create(user_id, data.model_dump())


@router.get("", response_model=list[Expense])
def list_expenses(
    category_id: int | None = None,
    min_amount: Decimal | None = Query(default=None, gt=0),
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: ExpenseService = Depends(get_expense_service),
    user_id: int = Depends(get_current_user_id),
):
    return service.list_for_user(
        user_id,
        category_id=category_id,
        min_amount=min_amount,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )


@router.get("/summary")
def get_summary(
    service: ExpenseService = Depends(get_expense_service),
    user_id: int = Depends(get_current_user_id),
):
    return service.summary(user_id)


@router.get("/by-category")
def by_category(
    service: ExpenseService = Depends(get_expense_service),
    user_id: int = Depends(get_current_user_id),
):
    return service.by_category(user_id)


@router.get("/{expense_id}", response_model=Expense)
def get_expense(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
    user_id: int = Depends(get_current_user_id),
):
    return service.get(expense_id, user_id)


@router.put("/{expense_id}", response_model=Expense)
def update_expense(
    expense_id: int,
    data: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
    user_id: int = Depends(get_current_user_id),
):
    return service.update(expense_id, user_id, data.model_dump())


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
    user_id: int = Depends(get_current_user_id),
):
    service.delete(expense_id, user_id)