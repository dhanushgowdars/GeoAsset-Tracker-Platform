from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetRepository:
    @staticmethod
    def create(db: Session, asset: AssetCreate) -> Asset:
        db_asset = Asset(**asset.model_dump())
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset

    @staticmethod
    def get_all(db: Session):
        return db.query(Asset).all()

    @staticmethod
    def get_by_id(db: Session, asset_id: int):
        return db.query(Asset).filter(Asset.id == asset_id).first()

    @staticmethod
    def update(db: Session, db_asset: Asset, asset: AssetUpdate):
        update_data = asset.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_asset, key, value)

        db.commit()
        db.refresh(db_asset)
        return db_asset

    @staticmethod
    def delete(db: Session, db_asset: Asset):
        db.delete(db_asset)
        db.commit()
