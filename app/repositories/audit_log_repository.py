from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditLogRepository:

    @staticmethod
    def create(
        db: Session,
        user_id: int | None,
        entity: str,
        entity_id: int,
        action: str,
        details: dict | None = None,
    ) -> AuditLog:

        audit_log = AuditLog(
            user_id=user_id,
            entity=entity,
            entity_id=entity_id,
            action=action,
            details=details,
        )

        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)

        return audit_log

    @staticmethod
    def get_all(
        db: Session,
    ):
        return (
            db.query(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .all()
        )