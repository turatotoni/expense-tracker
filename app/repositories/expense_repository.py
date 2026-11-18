from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, user_id: int, **fields) -> Expense:
        expense = Expense(user_id=user_id, **fields)
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get(self, expense_id: int) -> Expense | None:
        return self.db.get(Expense, expense_id)

    def list_for_user(
        self,
        user_id: int,
        category_id: int | None,
        min_amount: Decimal | None,
        date_from: date | None,
        date_to: date | None,
        limit: int,
        offset: int,
    ) -> list[Expense]:
        stmt = select(Expense).where(Expense.user_id == user_id)
        if category_id is not None:
            stmt = stmt.where(Expense.category_id == category_id)
        if min_amount is not None:
            stmt = stmt.where(Expense.amount >= min_amount)
        if date_from:
            stmt = stmt.where(Expense.spent_on >= date_from)
        if date_to:
            stmt = stmt.where(Expense.spent_on <= date_to)
        stmt = stmt.order_by(Expense.spent_on.desc(), Expense.id.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt).all())

    def update(self, expense: Expense, fields: dict) -> Expense:
        for field, value in fields.items():
            setattr(expense, field, value)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete(self, expense: Expense) -> None:
        self.db.delete(expense)
        self.db.commit()

    def summary(self, user_id: int) -> tuple[int, Decimal]:
        stmt = select(func.count(Expense.id), func.coalesce(func.sum(Expense.amount), 0)).where(
            Expense.user_id == user_id
        )
        count, total = self.db.execute(stmt).one()
        return count, total

    def totals_by_category(self, user_id: int) -> list[tuple[str, int, Decimal]]:
        stmt = (
            select(Category.name, func.count(Expense.id), func.sum(Expense.amount))
            .join(Category, Category.id == Expense.category_id)
            .where(Expense.user_id == user_id)
            .group_by(Category.name)
            .order_by(Category.name)
        )
        return [tuple(row) for row in self.db.execute(stmt).all()]