from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.enums.sort_field import SortField
from app.core.enums.sort_order import SortOrder
from app.schemas.pagination import PaginatedResponse
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
    BufferResponse,
    PolygonRequest,
    AreaResponse,
    CentroidResponse,
    RouteRequest,
    RouteLengthResponse,
    RouteIntersectionRequest,
    RouteIntersectionResponse,
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
    response_model=PaginatedResponse[AssetResponse],
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
    sort_by: SortField = Query(
        default=SortField.CREATED_AT,
        description="Field to sort by",
    ),
    order: SortOrder = Query(
        default=SortOrder.DESC,
        description="Sort order",
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
        sort_by=sort_by,
        order=order,
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

@router.get(
    "/{asset_id}/buffer",
    response_model=BufferResponse,
)
def generate_buffer(
    asset_id: int,
    radius_m: float = Query(
        ...,
        gt=0,
        description="Buffer radius in meters",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a buffer around an asset.
    """

    return AssetService.generate_buffer(
        db=db,
        current_user=current_user,
        asset_id=asset_id,
        radius_m=radius_m,
    )


@router.post(
    "/polygon/area",
    response_model=AreaResponse,
)
def calculate_polygon_area(
    request: PolygonRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Calculate polygon area.
    """

    return AssetService.calculate_polygon_area(
        db=db,
        current_user=current_user,
        polygon_points=request.coordinates,
    )


@router.post(
    "/polygon/centroid",
    response_model=CentroidResponse,
)
def calculate_polygon_centroid(
    request: PolygonRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Calculate polygon centroid.
    """

    return AssetService.calculate_polygon_centroid(
        db=db,
        current_user=current_user,
        polygon_points=request.coordinates,
    )

@router.post(
    "/route/length",
    response_model=RouteLengthResponse,
)
def calculate_route_length(
    request: RouteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Calculate the total length of a route.
    """

    return AssetService.calculate_route_length(
        db=db,
        current_user=current_user,
        coordinates=request.coordinates,
    )

@router.post(
    "/route/intersects",
    response_model=RouteIntersectionResponse,
)
def check_route_intersection(
    request: RouteIntersectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Check whether a route intersects a polygon.
    """

    return AssetService.check_route_intersection(
        db=db,
        current_user=current_user,
        route=request.route,
        polygon=request.polygon,
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
