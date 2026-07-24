from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.core.enums.asset_status import AssetStatus
from app.core.enums.asset_type import AssetType


class AnalyticsRepository:

    @staticmethod
    def get_summary(
        db: Session,
        owner_id: int,
    ):
        total_assets = (
            db.query(func.count(Asset.id))
            .filter(
                Asset.owner_id == owner_id,
                Asset.deleted_at.is_(None),
            )
            .scalar()
        )

        online_assets = (
            db.query(func.count(Asset.id))
            .filter(
                Asset.owner_id == owner_id,
                Asset.status == AssetStatus.ONLINE,
                Asset.deleted_at.is_(None),
            )
            .scalar()
        )

        offline_assets = (
            db.query(func.count(Asset.id))
            .filter(
                Asset.owner_id == owner_id,
                Asset.status == AssetStatus.OFFLINE,
                Asset.deleted_at.is_(None),
            )
            .scalar()
        )

        maintenance_assets = (
            db.query(func.count(Asset.id))
            .filter(
                Asset.owner_id == owner_id,
                Asset.status == AssetStatus.MAINTENANCE,
                Asset.deleted_at.is_(None),
            )
            .scalar()
        )

        retired_assets = (
            db.query(func.count(Asset.id))
            .filter(
                Asset.owner_id == owner_id,
                Asset.status == AssetStatus.RETIRED,
                Asset.deleted_at.is_(None),
            )
            .scalar()
        )

        assets_by_type = {}

        for asset_type in AssetType:
            assets_by_type[asset_type.value] = (
                db.query(func.count(Asset.id))
                .filter(
                    Asset.owner_id == owner_id,
                    Asset.asset_type == asset_type,
                    Asset.deleted_at.is_(None),
                )
                .scalar()
            )

        return {
            "total_assets": total_assets,
            "online_assets": online_assets,
            "offline_assets": offline_assets,
            "maintenance_assets": maintenance_assets,
            "retired_assets": retired_assets,
            "assets_by_type": assets_by_type,
        }