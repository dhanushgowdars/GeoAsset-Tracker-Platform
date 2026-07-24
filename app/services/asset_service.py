from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetService:
    # ==========================================================
    # CRUD OPERATIONS
    # ==========================================================

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
    ):
        """
        Get all assets belonging to the current user,
        optionally filtered by asset type, status, and search query.
        """

        return AssetRepository.get_all(
            db=db,
            owner_id=current_user.id,
            asset_type=asset_type,
            status=status,
            search=search,
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
    def update_asset(
        db: Session,
        asset_id: int,
        asset_update: AssetUpdate,
        current_user: User,
    ):
        """
        Update an asset.
        """

        db_asset = AssetRepository.get_by_id(
            db=db,
            asset_id=asset_id,
            owner_id=current_user.id,
        )

        if db_asset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found.",
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

        db_asset = AssetRepository.get_by_id(
            db=db,
            asset_id=asset_id,
            owner_id=current_user.id,
        )

        if db_asset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found.",
            )

        AssetRepository.delete(
            db=db,
            db_asset=db_asset,
        )

        return {"message": "Asset deleted successfully."}

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
