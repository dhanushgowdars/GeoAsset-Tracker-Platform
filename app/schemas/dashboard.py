from pydantic import BaseModel

from app.core.enums.asset_type import AssetType


class StatusSummary(BaseModel):
    total_assets: int
    online_assets: int
    offline_assets: int
    maintenance_assets: int
    retired_assets: int


class AssetTypeSummary(BaseModel):
    asset_type: AssetType
    count: int


class DashboardSummaryResponse(BaseModel):
    status_summary: StatusSummary
    asset_type_summary: list[AssetTypeSummary]