from sqlalchemy.orm import Session

from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetService:
    @staticmethod
    def create_asset(db: Session, asset: AssetCreate):
        return AssetRepository.create(db, asset)

    @staticmethod
    def get_all_assets(db: Session):
        return AssetRepository.get_all(db)

    @staticmethod
    def get_asset_by_id(db: Session, asset_id: int):
        return AssetRepository.get_by_id(db, asset_id)

    @staticmethod
    def update_asset(db: Session, db_asset, asset: AssetUpdate):
        return AssetRepository.update(db, db_asset, asset)

    @staticmethod
    def delete_asset(db: Session, db_asset):
        AssetRepository.delete(db, db_asset)
