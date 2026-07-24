from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums.sort_field import SortField
from app.core.enums.sort_order import SortOrder
from app.models.user import User
from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetService:
# ==========================================================
# CRUD OPERATIONS
# ==========================================================

    @staticmethod
    def _get_existing_asset(
        db: Session,
        asset_id: int,
        current_user: User,
    ):
        """
        Returns an existing asset owned by the current user.
        Raises 404 if the asset does not exist.
        """

        asset = AssetRepository.get_by_id(
            db=db,
            asset_id=asset_id,
            owner_id=current_user.id,
        )

        if asset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found.",
            )

        return asset


    @staticmethod
    def create_asset(
        db: Session,
        asset: AssetCreate,
        current_user: User,
    ):
        """
        Create a new asset.
        """

        return AssetRepository.create(
            db=db,
            asset=asset,
            owner_id=current_user.id,
        )


    @staticmethod
    def get_all_assets(
        db: Session,
        current_user: User,
        asset_type: str | None = None,
        status: str | None = None,
        search: str | None = None,
        sort_by: SortField = SortField.CREATED_AT,
        order: SortOrder = SortOrder.DESC,
        limit: int = 10,
        offset: int = 0,
    ):
        """
        Get paginated assets belonging to the current user
        with filtering, searching, sorting, and pagination.
        """

        return AssetRepository.get_all(
            db=db,
            owner_id=current_user.id,
            asset_type=asset_type,
            status=status,
            search=search,
            sort_by=sort_by,
            order=order,
            limit=limit,
            offset=offset,
        )


    @staticmethod
    def get_asset(
        db: Session,
        asset_id: int,
        current_user: User,
    ):
        """
        Get a single asset.
        """

        return AssetService._get_existing_asset(
            db=db,
            asset_id=asset_id,
            current_user=current_user,
        )


    @staticmethod
    def update_asset(
        db: Session,
        asset_id: int,
        asset_update: AssetUpdate,
        current_user: User,
    ):
        """
        Update an asset.
        """

        db_asset = AssetService._get_existing_asset(
            db=db,
            asset_id=asset_id,
            current_user=current_user,
        )

        return AssetRepository.update(
            db=db,
            db_asset=db_asset,
            asset=asset_update,
        )


    @staticmethod
    def delete_asset(
        db: Session,
        asset_id: int,
        current_user: User,
    ):
        """
        Delete an asset.
        """

        db_asset = AssetService._get_existing_asset(
            db=db,
            asset_id=asset_id,
            current_user=current_user,
        )

        AssetRepository.delete(
            db=db,
            db_asset=db_asset,
        )

        return {
            "message": "Asset deleted successfully."
        }

    # ==========================================================
    # GEOSPATIAL OPERATIONS
    # ==========================================================
    @staticmethod
    def get_nearby_assets(
        db: Session,
        current_user: User,
        latitude: float,
        longitude: float,
        radius_km: float,
        limit: int = 20,
        offset: int = 0,
    ):
        """
        Get all nearby assets within the given radius.
        """

        if radius_km <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Radius must be greater than zero.",
            )

        nearby_assets = AssetRepository.get_nearby_assets(
            db=db,
            owner_id=current_user.id,
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            limit=limit,
            offset=offset,
        )

        response = []

        for asset, distance in nearby_assets:
            response.append(
    {
        "id": asset.id,
        "serial_number": asset.serial_number,
        "asset_type": asset.asset_type,
        "status": asset.status,
        "name": asset.name,
        "description": asset.description,
        "latitude": asset.latitude,
        "longitude": asset.longitude,
        "owner_id": asset.owner_id,
        "created_at": asset.created_at,
        "distance_km": round(distance, 3),
    }
)

        return response

    @staticmethod
    def get_nearest_asset(
        db: Session,
        current_user: User,
        latitude: float,
        longitude: float,
    ):
        """
        Get the nearest asset.
        """

        nearest = AssetRepository.get_nearest_asset(
            db=db,
            owner_id=current_user.id,
            latitude=latitude,
            longitude=longitude,
        )

        if nearest is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No assets found.",
            )

        asset, distance = nearest

        return {
    "id": asset.id,
    "serial_number": asset.serial_number,
    "asset_type": asset.asset_type,
    "status": asset.status,
    "name": asset.name,
    "description": asset.description,
    "latitude": asset.latitude,
    "longitude": asset.longitude,
    "owner_id": asset.owner_id,
    "created_at": asset.created_at,
    "distance_km": round(distance, 3),
}

    @staticmethod
    def calculate_distance(
        db: Session,
        current_user: User,
        asset_id: int,
        latitude: float,
        longitude: float,
    ):
        """
        Calculate the distance from the given location
        to a specific asset.
        """

        result = AssetRepository.calculate_distance_to_asset(
            db=db,
            asset_id=asset_id,
            owner_id=current_user.id,
            latitude=latitude,
            longitude=longitude,
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found.",
            )

        return {
            "asset_id": result.id,
            "distance_km": round(result.distance_km, 3),
        }

    @staticmethod
    def get_assets_in_bounding_box(
        db: Session,
        current_user: User,
        min_latitude: float,
        min_longitude: float,
        max_latitude: float,
        max_longitude: float,
    ):
        """
        Get all assets inside a bounding box.
        """

        assets = AssetRepository.get_assets_in_bounding_box(
            db=db,
            owner_id=current_user.id,
            min_latitude=min_latitude,
            min_longitude=min_longitude,
            max_latitude=max_latitude,
            max_longitude=max_longitude,
        )

        return assets

    @staticmethod
    def get_assets_in_geofence(
        db: Session,
        current_user: User,
        polygon_points: list[list[float]],
    ):
        """
        Get all assets inside a custom polygon.
        """

        if len(polygon_points) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A polygon must contain at least three points.",
            )

        assets = AssetRepository.get_assets_in_geofence(
            db=db,
            owner_id=current_user.id,
            polygon_points=polygon_points,
        )

        return assets

    @staticmethod
    def generate_buffer(
        db: Session,
        current_user: User,
        asset_id: int,
        radius_m: float,
    ):
        """
        Generate a buffer around an asset.
        """

        AssetService._get_existing_asset(
            db=db,
            asset_id=asset_id,
            current_user=current_user,
        )

        result = AssetRepository.generate_buffer(
            db=db,
            asset_id=asset_id,
            owner_id=current_user.id,
            radius_m=radius_m,
        )

        return {
            "asset_id": result.asset_id,
            "radius_m": radius_m,
            "buffer_wkt": result.buffer_wkt,
        }

    @staticmethod
    def calculate_polygon_area(
        db: Session,
        current_user: User,
        polygon_points: list[list[float]],
    ):
        """
        Calculate the area of a polygon.
        """

        area = AssetRepository.calculate_polygon_area(
            db=db,
            polygon_points=polygon_points,
        )

        return {
            "area_sq_m": round(area, 3),
        }

    @staticmethod
    def calculate_polygon_centroid(
        db: Session,
        current_user: User,
        polygon_points: list[list[float]],
    ):
        """
        Calculate the centroid of a polygon.
        """

        centroid = AssetRepository.calculate_polygon_centroid(
            db=db,
            polygon_points=polygon_points,
        )

        return centroid
    @staticmethod
    def calculate_route_length(
        db: Session,
        current_user: User,
        coordinates: list[list[float]],
    ):
        """
        Calculate the total route length.
        """

        if len(coordinates) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A route must contain at least two points.",
            )

        length = AssetRepository.calculate_route_length(
            db=db,
            coordinates=coordinates,
        )

        return {
            "length_m": round(length, 3),
        }


    @staticmethod
    def check_route_intersection(
        db: Session,
        current_user: User,
        route: list[list[float]],
        polygon: list[list[float]],
    ):
        """
        Check whether a route intersects a polygon.
        """

        if len(route) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Route must contain at least two points.",
            )

        if len(polygon) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Polygon must contain at least three points.",
            )

        intersects = AssetRepository.check_route_intersection(
            db=db,
            route=route,
            polygon=polygon,
        )

        return {
            "intersects": intersects,
        }