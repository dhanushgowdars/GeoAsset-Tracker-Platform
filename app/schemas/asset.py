from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AssetCreate(BaseModel):
    """
    Schema used when creating a new asset.
    """

    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    latitude: float
    longitude: float


class AssetUpdate(BaseModel):
    """
    Schema used when updating an existing asset.
    All fields are optional.
    """

    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AssetResponse(BaseModel):
    """
    Schema returned to the client.
    """

    id: int
    name: str
    description: Optional[str]
    latitude: float
    longitude: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
