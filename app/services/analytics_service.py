from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    @staticmethod
    def get_summary(
        db: Session,
        current_user: User,
    ):
        return AnalyticsRepository.get_summary(
            db=db,
            owner_id=current_user.id,
        )