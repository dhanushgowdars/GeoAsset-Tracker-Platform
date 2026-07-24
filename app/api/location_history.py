from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.location_history import LocationHistoryListResponse
from app.services.location_history_service import LocationHistoryService

router = APIRouter(
    prefix="/location-history",
    tags=["Location History"],
)


@router.get(
    "/{asset_id}",
    response_model=LocationHistoryListResponse,
)
def get_location_history(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    history = LocationHistoryService.get_location_history(
        db=db,
        asset_id=asset_id,
    )

    return {
        "history": history,
    }