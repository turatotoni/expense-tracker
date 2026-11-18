from app.exceptions import InvalidInputError, NotFoundError
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository


class ExpenseService:
    def __init__(self, expenses: ExpenseRepository, categories: CategoryRepository):
        self.expenses = expenses
        self.categories = categories

    def _check_category(self, category_id: int, user_id: int) -> None:
        if not self.categories.exists_for_user(category_id, user_id):
            raise InvalidInputError("Invalid category_id")

    def _get_own(self, expense_id: int, user_id: int):
        expense = self.expenses.get(expense_id)
        if expense is None or expense.user_id != user_id:
            raise NotFoundError("Expense not found")
        return expense

    def create(self, user_id: int, fields: dict):
        self._check_category(fields["category_id"], user_id)
        return self.expenses.add(user_id, **fields)

    def get(self, expense_id: int, user_id: int):
        return self._get_own(expense_id, user_id)

    def list_for_user(self, user_id: int, **filters):
        return self.expenses.list_for_user(user_id, **filters)

    def update(self, expense_id: int, user_id: int, fields: dict):
        expense = self._get_own(expense_id, user_id)
        self._check_category(fields["category_id"], user_id)
        return self.expenses.update(expense, fields)

    def delete(self, expense_id: int, user_id: int) -> None:
        expense = self._get_own(expense_id, user_id)
        self.expenses.delete(expense)

    def summary(self, user_id: int) -> dict:
        count, total = self.expenses.summary(user_id)
        return {"number_of_expenses": count, "sum_of_expenses": total}

    def by_category(self, user_id: int) -> list[dict]:
        return [
            {"category": name, "count": count, "total": total}
            for name, count, total in self.expenses.totals_by_category(user_id)
        ]