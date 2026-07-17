from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.roles import UserRole
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.USER,
    )
    assets = relationship(
        "Asset",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
