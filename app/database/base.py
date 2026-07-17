from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here so SQLAlchemy knows about them
from app.models.asset import Asset
