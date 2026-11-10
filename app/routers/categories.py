from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models.category import Category as CategoryModel
from app.schemas.category import Category, CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    category = CategoryModel(user_id=user_id, name=data.name)
    db.add(category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category already exists")
    db.refresh(category)
    return category


@router.get("", response_model=list[Category])
def list_categories(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    stmt = select(CategoryModel).where(CategoryModel.user_id == user_id).order_by(CategoryModel.name)
    return db.scalars(stmt).all()