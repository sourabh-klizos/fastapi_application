from typing import Optional
from fastapi import HTTPException, status


async def is_logged_in_and_admin(
    logged_in_user: dict, raise_error: bool = True
) -> bool:
    if logged_in_user is None:
        if raise_error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return False

    if logged_in_user["role"] != "admin":
        if raise_error:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to perform this action",
            )
        return False

    return True
