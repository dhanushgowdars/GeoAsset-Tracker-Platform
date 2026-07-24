from datetime import datetime

from sqlalchemy import cast, func
from sqlalchemy.orm import Session

from geoalchemy2 import Geography
from geoalchemy2.elements import WKTElement

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetRepository:
    # ==========================================================
    # CRUD OPERATIONS
    # ==========================================================

    @staticmethod
    def create(
        db: Session,
        asset: AssetCreate,
        owner_id: int,
    ) -> Asset:

        db_asset = Asset(
            **asset.model_dump(),
            owner_id=owner_id,
            location=WKTElement(
                f"POINT({asset.longitude} {asset.latitude})",
                srid=4326,
            ),
        )

        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)

        return db_asset

    
    @staticmethod
    def get_all(
        db: Session,
        owner_id: int,
        asset_type: str | None = None,
        status: str | None = None,
    ):
        query = (
            db.query(Asset)
            .filter(
                Asset.owner_id == owner_id,
                Asset.deleted_at.is_(None),
            )
        )

        if asset_type:
            query = query.filter(
                Asset.asset_type == asset_type,
            )

        if status:
            query = query.filter(
                Asset.status == status,
            )

        return query.all()

    @staticmethod
    def get_by_id(
        db: Session,
        asset_id: int,
        owner_id: int,
    ):
        return (
            db.query(Asset)
            .filter(
                Asset.id == asset_id,
                Asset.owner_id == owner_id,
                Asset.deleted_at.is_(None),
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        db_asset: Asset,
        asset: AssetUpdate,
    ):

        update_data = asset.model_dump(
            exclude_unset=True,
        )

        for key, value in update_data.items():
            setattr(
                db_asset,
                key,
                value,
            )

        if "latitude" in update_data or "longitude" in update_data:
            latitude = update_data.get(
                "latitude",
                db_asset.latitude,
            )

            longitude = update_data.get(
                "longitude",
                db_asset.longitude,
            )

            db_asset.location = WKTElement(
                f"POINT({longitude} {latitude})",
                srid=4326,
            )

            db_asset.last_location_update = datetime.utcnow()

        db.commit()
        db.refresh(db_asset)

        return db_asset

    @staticmethod
    def delete(
        db: Session,
        db_asset: Asset,
    ):
        db_asset.deleted_at = datetime.utcnow()

        db.commit()
        db.refresh(db_asset)

        return db_asset
    # ==========================================================
    # GEOSPATIAL OPERATIONS
    # ==========================================================
    @staticmethod
    def get_nearby_assets(
        db: Session,
        owner_id: int,
        latitude: float,
        longitude: float,
        radius_km: float,
        limit: int = 20,
        offset: int = 0,
    ):
        """
        Returns all assets within the specified radius,
        ordered by distance from the given location.
        """

        search_point = WKTElement(
            f"POINT({longitude} {latitude})",
            srid=4326,
        )

        distance = (
            func.ST_Distance(
                cast(Asset.location, Geography),
                cast(search_point, Geography),
            )
            / 1000.0
        ).label("distance_km")

        nearby_assets = (
            db.query(
                Asset,
                distance,
            )
            .filter(
                Asset.owner_id == owner_id,
                Asset.deleted_at.is_(None),
                func.ST_DWithin(
                    cast(Asset.location, Geography),
                    cast(search_point, Geography),
                    radius_km * 1000,
                ),
            )
            .order_by(distance.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return nearby_assets

    @staticmethod
    def get_nearest_asset(
        db: Session,
        owner_id: int,
        latitude: float,
        longitude: float,
    ):
        """
        Returns the nearest asset to the given location.
        """

        search_point = WKTElement(
            f"POINT({longitude} {latitude})",
            srid=4326,
        )

        distance = (
            func.ST_Distance(
                cast(Asset.location, Geography),
                cast(search_point, Geography),
            )
            / 1000.0
        ).label("distance_km")

        nearest_asset = (
            db.query(
                Asset,
                distance,
            )
            .filter(
                Asset.owner_id == owner_id,
                Asset.deleted_at.is_(None),
            )
            .order_by(distance.asc())
            .first()
        )

        return nearest_asset

    @staticmethod
    def calculate_distance_to_asset(
        db: Session,
        asset_id: int,
        owner_id: int,
        latitude: float,
        longitude: float,
    ):
        """
        Calculates the distance between the given location
        and a specific asset.
        """

        search_point = WKTElement(
            f"POINT({longitude} {latitude})",
            srid=4326,
        )

        distance = (
            func.ST_Distance(
                cast(Asset.location, Geography),
                cast(search_point, Geography),
            )
            / 1000.0
        ).label("distance_km")

        result = (
            db.query(
                Asset.id,
                distance,
            )
            .filter(
                Asset.id == asset_id,
                Asset.owner_id == owner_id,
                Asset.deleted_at.is_(None),
            )
            .first()
        )

        return result

    @staticmethod
    def get_assets_in_bounding_box(
        db: Session,
        owner_id: int,
        min_latitude: float,
        min_longitude: float,
        max_latitude: float,
        max_longitude: float,
    ):
        """
        Returns all assets inside the given
        latitude/longitude bounding box.
        """

        bounding_box = func.ST_MakeEnvelope(
            min_longitude,
            min_latitude,
            max_longitude,
            max_latitude,
            4326,
        )

        assets = (
            db.query(Asset)
            .filter(
                Asset.owner_id == owner_id,
                Asset.deleted_at.is_(None),
                func.ST_Within(
                    Asset.location,
                    bounding_box,
                ),
            )
            .all()
        )

        return assets

    @staticmethod
    def get_assets_in_geofence(
        db: Session,
        owner_id: int,
        polygon_points: list[list[float]],
    ):
        """
        Returns all assets inside a custom geofence polygon.

        polygon_points format:
        [
            [longitude, latitude],
            [longitude, latitude],
            ...
        ]

        Note:
        The first and last point must be the same to
        close the polygon. If they are not, this
        method will automatically close it without
        modifying the original input list.
        """

        if len(polygon_points) < 3:
            raise ValueError("A polygon must contain at least three points.")

        # Create a closed polygon without mutating the original input
        if polygon_points[0] == polygon_points[-1]:
            closed_polygon = polygon_points
        else:
            closed_polygon = polygon_points + [polygon_points[0]]

        polygon_coordinates = ", ".join(
            f"{longitude} {latitude}" for longitude, latitude in closed_polygon
        )

        polygon_wkt = f"POLYGON(({polygon_coordinates}))"

        polygon = func.ST_GeomFromText(
            polygon_wkt,
            4326,
        )

        assets = (
            db.query(Asset)
            .filter(
                Asset.owner_id == owner_id,
                Asset.deleted_at.is_(None),
                func.ST_Contains(
                    polygon,
                    Asset.location,
                ),
            )
            .all()
        )

        return assets
