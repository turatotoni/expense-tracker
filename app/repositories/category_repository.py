from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, user_id: int, name: str) -> Category:
        category = Category(user_id=user_id, name=name)
        self.db.add(category)
        self.db.commit()          # IntegrityError se propušta service sloju
        self.db.refresh(category)
        return category

    def list_for_user(self, user_id: int) -> list[Category]:
        stmt = select(Category).where(Category.user_id == user_id).order_by(Category.name)
        return list(self.db.scalars(stmt).all())

    def exists_for_user(self, category_id: int, user_id: int) -> bool:
        stmt = select(Category.id).where(Category.id == category_id, Category.user_id == user_id)
        return self.db.scalar(stmt) is not None

    def rollback(self) -> None:
        self.db.rollback()