from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.db.dependencies import get_user_service
from app.db.models import User
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_by_id(
    user_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    user = await service.get_by_id(user_id)

    if current_user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return user
