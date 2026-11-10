from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models.category import Category as CategoryModel
from app.models.expense import Expense as ExpenseModel
from app.schemas.expense import Expense, ExpenseCreate

router = APIRouter(prefix="/expenses", tags=["expenses"])


def _check_category(db: Session, category_id: int, user_id: int) -> None:
    """Kategorija mora postojati i pripadati ovom korisniku."""
    stmt = select(CategoryModel.id).where(
        CategoryModel.id == category_id, CategoryModel.user_id == user_id
    )
    if db.scalar(stmt) is None:
        raise HTTPException(status_code=400, detail="Invalid category_id")


@router.post("", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    _check_category(db, data.category_id, user_id)
    expense = ExpenseModel(user_id=user_id, **data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=list[Expense])
def list_expenses(
    category_id: int | None = None,
    min_amount: Decimal | None = Query(default=None, gt=0),
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    stmt = select(ExpenseModel).where(ExpenseModel.user_id == user_id)
    if category_id is not None:
        stmt = stmt.where(ExpenseModel.category_id == category_id)
    if min_amount is not None:
        stmt = stmt.where(ExpenseModel.amount >= min_amount)
    if date_from:
        stmt = stmt.where(ExpenseModel.spent_on >= date_from)
    if date_to:
        stmt = stmt.where(ExpenseModel.spent_on <= date_to)
    stmt = stmt.order_by(ExpenseModel.spent_on.desc(), ExpenseModel.id.desc())
    stmt = stmt.limit(limit).offset(offset)
    return db.scalars(stmt).all()


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    stmt = select(func.count(ExpenseModel.id), func.coalesce(func.sum(ExpenseModel.amount), 0)).where(
        ExpenseModel.user_id == user_id
    )
    count, total = db.execute(stmt).one()
    return {"number_of_expenses": count, "sum_of_expenses": total}


@router.get("/by-category")
def by_category(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    stmt = (
        select(CategoryModel.name, func.count(ExpenseModel.id), func.sum(ExpenseModel.amount))
        .join(CategoryModel, CategoryModel.id == ExpenseModel.category_id)
        .where(ExpenseModel.user_id == user_id)
        .group_by(CategoryModel.name)
        .order_by(CategoryModel.name)
    )
    return [
        {"category": name, "count": count, "total": total}
        for name, count, total in db.execute(stmt).all()
    ]


def _get_own_expense(db: Session, expense_id: int, user_id: int) -> ExpenseModel:
    expense = db.get(ExpenseModel, expense_id)
    if expense is None or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.get("/{expense_id}", response_model=Expense)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return _get_own_expense(db, expense_id, user_id)


@router.put("/{expense_id}", response_model=Expense)
def update_expense(
    expense_id: int,
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    expense = _get_own_expense(db, expense_id, user_id)
    _check_category(db, data.category_id, user_id)
    for field, value in data.model_dump().items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    expense = _get_own_expense(db, expense_id, user_id)
    db.delete(expense)
    db.commit()