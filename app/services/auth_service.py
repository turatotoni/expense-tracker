from sqlalchemy.exc import IntegrityError

from app.exceptions import ConflictError, UnauthorizedError
from app.repositories.user_repository import UserRepository
from app.security import create_access_token, hash_password, verify_password


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

    def register(self, email: str, password: str):
        try:
            return self.users.add(email.lower(), hash_password(password))
        except IntegrityError:
            self.users.rollback()
            raise ConflictError("Email already registered")

    def login(self, email: str, password: str) -> str:
        user = self.users.get_by_email(email.lower())
        if user is None or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Incorrect email or password")
        return create_access_token(user.id)

    def get_user(self, user_id: int):
        return self.users.get(user_id)