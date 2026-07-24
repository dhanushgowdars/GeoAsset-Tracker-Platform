from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository


class AuditLogService:

    @staticmethod
    def log_action(
        db: Session,
        user_id: int | None,
        entity: str,
        entity_id: int,
        action: str,
        details: dict | None = None,
    ) -> AuditLog:
        return AuditLogRepository.create(
            db=db,
            user_id=user_id,
            entity=entity,
            entity_id=entity_id,
            action=action,
            details=details,
        )

    @staticmethod
    def get_all_logs(
        db: Session,
    ):
        return AuditLogRepository.get_all(db)