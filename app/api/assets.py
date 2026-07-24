from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.enums.asset_type import AssetType
from app.core.enums.asset_status import AssetStatus

from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.asset import (
    AssetCreate,
    AssetResponse,
    AssetUpdate,
    NearbyAssetResponse,
    DistanceResponse,
    BoundingBoxResponse,
    GeofenceRequest,
)
from app.services.asset_service import AssetService

router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
)


# ==========================================================
# CRUD ENDPOINTS
# ==========================================================


@router.post(
    "/",
    response_model=AssetResponse,
    status_code=201,
)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AssetService.create_asset(
        db=db,
        asset=asset,
        current_user=current_user,
    )


@router.get(
    "/",
    response_model=List[AssetResponse],
)
def get_all_assets(
    asset_type: AssetType | None = Query(
        default=None,
        description="Filter by asset type",
    ),
    status: AssetStatus | None = Query(
        default=None,
        description="Filter by asset status",
    ),
    search: str | None = Query(
        default=None,
        description="Search by asset name, serial number, or description",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of assets to return",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of assets to skip",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AssetService.get_all_assets(
        db=db,
        current_user=current_user,
        asset_type=asset_type,
        status=status,
        search=search,
        limit=limit,
        offset=offset,
    )


# ==========================================================
# GEOSPATIAL ENDPOINTS
# ==========================================================
@router.get(
    "/nearby",
    response_model=list[NearbyAssetResponse],
)
def get_nearby_assets(
    latitude: float = Query(
        ...,
        description="Current latitude",
    ),
    longitude: float = Query(
        ...,
        description="Current longitude",
    ),
    radius_km: float = Query(
        ...,
        gt=0,
        description="Search radius in kilometers",
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        0,
        ge=0,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all assets within a specified radius.
    """

    return AssetService.get_nearby_assets(
        db=db,
        current_user=current_user,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/nearest",
    response_model=NearbyAssetResponse,
)
def get_nearest_asset(
    latitude: float = Query(
        ...,
        description="Current latitude",
    ),
    longitude: float = Query(
        ...,
        description="Current longitude",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the nearest asset to the given location.
    """

    return AssetService.get_nearest_asset(
        db=db,
        current_user=current_user,
        latitude=latitude,
        longitude=longitude,
    )


@router.get(
    "/{asset_id}/distance",
    response_model=DistanceResponse,
)
def calculate_distance(
    asset_id: int,
    latitude: float = Query(
        ...,
        description="Current latitude",
    ),
    longitude: float = Query(
        ...,
        description="Current longitude",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Calculate the distance from the given location
    to a specific asset.
    """

    return AssetService.calculate_distance(
        db=db,
        current_user=current_user,
        asset_id=asset_id,
        latitude=latitude,
        longitude=longitude,
    )


@router.get(
    "/bbox",
    response_model=list[BoundingBoxResponse],
)
def get_assets_in_bounding_box(
    min_latitude: float = Query(...),
    min_longitude: float = Query(...),
    max_latitude: float = Query(...),
    max_longitude: float = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all assets inside a bounding box.
    """

    return AssetService.get_assets_in_bounding_box(
        db=db,
        current_user=current_user,
        min_latitude=min_latitude,
        min_longitude=min_longitude,
        max_latitude=max_latitude,
        max_longitude=max_longitude,
    )


@router.post(
    "/geofence",
    response_model=list[AssetResponse],
)
def get_assets_in_geofence(
    request: GeofenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all assets inside a custom polygon.
    """

    return AssetService.get_assets_in_geofence(
        db=db,
        current_user=current_user,
        polygon_points=request.coordinates,
    )


@router.get(
    "/{asset_id}",
    response_model=AssetResponse,
)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AssetService.get_asset(
        db=db,
        asset_id=asset_id,
        current_user=current_user,
    )


@router.put(
    "/{asset_id}",
    response_model=AssetResponse,
)
def update_asset(
    asset_id: int,
    asset: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AssetService.update_asset(
        db=db,
        asset_id=asset_id,
        asset_update=asset,
        current_user=current_user,
    )


@router.delete(
    "/{asset_id}",
)
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AssetService.delete_asset(
        db=db,
        asset_id=asset_id,
        current_user=current_user,
    )
