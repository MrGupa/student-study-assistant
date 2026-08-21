from uuid import UUID

from fastapi import APIRouter, Depends

from app.db.dependencies import get_user_service
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):

    user = await service.get_by_id(user_id)

    return user
