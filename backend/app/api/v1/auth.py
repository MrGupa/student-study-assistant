from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.auth.jwt import create_access_token, create_refresh_token
from app.core.config import settings
from app.db.dependencies import get_auth_service
from app.schemas.auth import RegisteredUserResponse, RegistrationRequest, RegistrationResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/auth/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"],
)
async def register(
    payload: RegistrationRequest,
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> RegistrationResponse:
    """Register a new user and issue authentication tokens."""

    user = await service.register(
        email=str(payload.email),
        full_name=payload.full_name,
        password=payload.password,
    )

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
    )
    refresh_token = create_refresh_token(user_id=user.id)

    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=refresh_token,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite=settings.refresh_cookie_samesite,
        path=settings.refresh_cookie_path,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
    )

    return RegistrationResponse(
        user=RegisteredUserResponse.model_validate(user),
        access_token=access_token,
    )
