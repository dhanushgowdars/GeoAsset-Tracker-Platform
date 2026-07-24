from pydantic import BaseModel


class AnalyticsSummaryResponse(BaseModel):
    total_assets: int
    online_assets: int
    offline_assets: int
    maintenance_assets: int
    retired_assets: int
    assets_by_type: dict[str, int]