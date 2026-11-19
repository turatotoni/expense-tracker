from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import decode_access_token

from app.repositories.category_repository import CategoryRepository
from app.services.category_service import CategoryService
from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> int:
    user_id = decode_access_token(token)
    if user_id is None or db.get(User, user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(db))

def get_expense_service(db: Session = Depends(get_db)) -> ExpenseService:
    return ExpenseService(ExpenseRepository(db), CategoryRepository(db))

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))