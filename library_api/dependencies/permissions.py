from fastapi import Depends, HTTPException, status

from library_api.core.security import get_current_user
from library_api.models.users import User, UserRole


def require_roles(*roles: UserRole):
    async def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='not enough permissions',
            )
        return current_user

    return checker
