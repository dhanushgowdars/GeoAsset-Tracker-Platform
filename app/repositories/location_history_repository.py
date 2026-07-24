from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_X, ST_Y
from sqlalchemy.orm import Session

from app.models.location_history import LocationHistory


class LocationHistoryRepository:

    @staticmethod
    def create(
        db: Session,
        asset_id: int,
        latitude: float,
        longitude: float,
    ) -> LocationHistory:

        history = LocationHistory(
            asset_id=asset_id,
            location=WKTElement(
                f"POINT({longitude} {latitude})",
                srid=4326,
            ),
        )

        db.add(history)
        db.commit()
        db.refresh(history)

        return history

    @staticmethod
    def get_history(
        db: Session,
        asset_id: int,
    ):
        return (
            db.query(
                LocationHistory.id,
                LocationHistory.asset_id,
                ST_Y(LocationHistory.location).label("latitude"),
                ST_X(LocationHistory.location).label("longitude"),
                LocationHistory.recorded_at,
            )
            .filter(LocationHistory.asset_id == asset_id)
            .order_by(
                LocationHistory.recorded_at.desc(),
                LocationHistory.id.desc(),
            )
            .all()
        )