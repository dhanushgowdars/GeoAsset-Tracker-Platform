from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.core.enums.roles import UserRole


def require_role(required_role: UserRole):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return role_checker
