from sqlalchemy.orm import Session

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
