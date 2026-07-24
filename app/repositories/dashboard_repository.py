from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.core.enums.asset_status import AssetStatus


class DashboardRepository:

    @staticmethod
    def get_dashboard_summary(db: Session):
        total_assets = (
            db.query(func.count(Asset.id))
            .filter(Asset.deleted_at.is_(None))
            .scalar()
        )

        online_assets = (
            db.query(func.count(Asset.id))
            .filter(
                Asset.deleted_at.is_(None),
                Asset.status == AssetStatus.ONLINE,
            )
            .scalar()
        )

        offline_assets = (
            db.query(func.count(Asset.id))
            .filter(
                Asset.deleted_at.is_(None),
                Asset.status == AssetStatus.OFFLINE,
            )
            .scalar()
        )

        maintenance_assets = (
            db.query(func.count(Asset.id))
            .filter(
                Asset.deleted_at.is_(None),
                Asset.status == AssetStatus.MAINTENANCE,
            )
            .scalar()
        )

        retired_assets = (
            db.query(func.count(Asset.id))
            .filter(
                Asset.deleted_at.is_(None),
                Asset.status == AssetStatus.RETIRED,
            )
            .scalar()
        )

        asset_type_summary = (
            db.query(
                Asset.asset_type,
                func.count(Asset.id).label("count"),
            )
            .filter(Asset.deleted_at.is_(None))
            .group_by(Asset.asset_type)
            .all()
        )

        return {
            "status_summary": {
                "total_assets": total_assets,
                "online_assets": online_assets,
                "offline_assets": offline_assets,
                "maintenance_assets": maintenance_assets,
                "retired_assets": retired_assets,
            },
            "asset_type_summary": [
                {
                    "asset_type": row.asset_type,
                    "count": row.count,
                }
                for row in asset_type_summary
            ],
        }