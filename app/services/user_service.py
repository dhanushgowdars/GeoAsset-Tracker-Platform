from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    @staticmethod
    def register_user(db: Session, user: UserCreate):
        existing_email = UserRepository.get_by_email(db, user.email)
        if existing_email:
            raise ValueError("Email already exists")

        existing_username = UserRepository.get_by_username(db, user.username)
        if existing_username:
            raise ValueError("Username already exists")

        return UserRepository.create(db, user)

    @staticmethod
    def login_user(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)

        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }
