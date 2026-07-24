from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None
    entity: str
    entity_id: int
    action: str
    details: dict[str, Any] | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)