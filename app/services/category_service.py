from sqlalchemy.exc import IntegrityError

from app.exceptions import ConflictError
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    def create(self, user_id: int, name: str):
        try:
            return self.repo.add(user_id, name)
        except IntegrityError:
            self.repo.rollback()
            raise ConflictError("Category already exists")

    def list_for_user(self, user_id: int):
        return self.repo.list_for_user(user_id)