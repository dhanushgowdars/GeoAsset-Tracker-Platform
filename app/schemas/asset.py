from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# CRUD SCHEMAS
# ==========================================================


class AssetCreate(BaseModel):
    """
    Schema used when creating a new asset.
    """

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )
    description: Optional[str] = None

    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )


class AssetUpdate(BaseModel):
    """
    Schema used when updating an existing asset.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    description: Optional[str] = None

    latitude: Optional[float] = Field(
        default=None,
        ge=-90,
        le=90,
    )

    longitude: Optional[float] = Field(
        default=None,
        ge=-180,
        le=180,
    )


class AssetResponse(BaseModel):
    """
    Standard CRUD response.
    """

    id: int
    name: str
    description: Optional[str]
    latitude: float
    longitude: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# GEO RESPONSE SCHEMAS
# ==========================================================


class NearbyAssetResponse(AssetResponse):
    """
    Returned by Nearby Assets and Nearest Asset endpoints.
    """

    distance_km: float


class DistanceResponse(BaseModel):
    """
    Returned when calculating distance
    between a coordinate and an asset.
    """

    asset_id: int
    distance_km: float


# ==========================================================
# BOUNDING BOX
# ==========================================================


class BoundingBoxResponse(AssetResponse):
    """
    Assets found inside a bounding box.
    """

    pass


# ==========================================================
# GEOFENCE
# ==========================================================


class GeofenceRequest(BaseModel):
    """
    Polygon coordinates.

    Example:

    [
        [76.63,12.29],
        [76.65,12.30],
        [76.64,12.32],
        [76.63,12.29]
    ]
    """

    coordinates: list[list[float]]
