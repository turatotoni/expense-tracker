from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_auth_service, get_current_user_id
from app.schemas.user import Token, User, UserCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, service: AuthService = Depends(get_auth_service)):
    return service.register(data.email, data.password)


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    # OAuth2 forma zove polje "username"; kod nas je to email
    return Token(access_token=service.login(form.username, form.password))


@router.get("/me", response_model=User)
def me(
    service: AuthService = Depends(get_auth_service),
    user_id: int = Depends(get_current_user_id),
):
    return service.get_user(user_id)