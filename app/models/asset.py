from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    description = Column(Text, nullable=True)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
