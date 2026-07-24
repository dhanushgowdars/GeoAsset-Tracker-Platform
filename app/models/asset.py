from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.database.base import Base
from app.core.enums.asset_type import AssetType
from app.core.enums.asset_status import AssetStatus


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    serial_number = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    asset_type = Column(
        Enum(AssetType, name="asset_type_enum"),
        nullable=False,
    )

    status = Column(
        Enum(AssetStatus, name="asset_status_enum"),
        nullable=False,
        default=AssetStatus.ONLINE,
    )

    name = Column(String(100), nullable=False)

    description = Column(Text, nullable=True)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    location = Column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
        ),
        nullable=False,
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="assets",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    last_location_update = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    location_history = relationship(
    "LocationHistory",
    back_populates="asset",
    cascade="all, delete-orphan",
)