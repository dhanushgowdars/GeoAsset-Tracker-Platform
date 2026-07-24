from sqlalchemy.orm import Session

from app.repositories.location_history_repository import (
    LocationHistoryRepository,
)


class LocationHistoryService:

    @staticmethod
    def create_location_history(
        db: Session,
        asset_id: int,
        latitude: float,
        longitude: float,
    ):
        return LocationHistoryRepository.create(
            db=db,
            asset_id=asset_id,
            latitude=latitude,
            longitude=longitude,
        )

    @staticmethod
    def get_location_history(
        db: Session,
        asset_id: int,
    ):
        return LocationHistoryRepository.get_history(
            db=db,
            asset_id=asset_id,
        )