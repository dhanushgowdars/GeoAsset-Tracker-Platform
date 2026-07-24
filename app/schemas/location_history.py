from datetime import datetime

from pydantic import BaseModel


class LocationHistoryResponse(BaseModel):
    id: int
    asset_id: int
    latitude: float
    longitude: float
    recorded_at: datetime

    model_config = {
        "from_attributes": True
    }


class LocationHistoryListResponse(BaseModel):
    history: list[LocationHistoryResponse]