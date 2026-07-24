from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.audit_log import AuditLogResponse
from app.services.audit_log_service import AuditLogService

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.get(
    "/",
    response_model=list[AuditLogResponse],
)
def get_audit_logs(
    db: Session = Depends(get_db),
):
    return AuditLogService.get_all_logs(db)