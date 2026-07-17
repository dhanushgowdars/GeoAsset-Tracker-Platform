from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService

from app.auth.dependencies import get_current_user
from app.auth.role_dependencies import require_role
from app.core.roles import UserRole

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        return UserService.register_user(db, user)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        return UserService.login_user(
            db,
            user.email,
            user.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )


@router.get("/admin")
def admin_only(
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return {
        "message": "Welcome Admin!",
        "username": current_user.username,
        "role": current_user.role.value,
    }
