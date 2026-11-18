from fastapi import APIRouter, Depends, status

from app.dependencies import get_category_service, get_current_user_id
from app.schemas.category import Category, CategoryCreate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
    user_id: int = Depends(get_current_user_id),
):
    return service.create(user_id, data.name)


@router.get("", response_model=list[Category])
def list_categories(
    service: CategoryService = Depends(get_category_service),
    user_id: int = Depends(get_current_user_id),
):
    return service.list_for_user(user_id)