from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response, status

from app.auth.jwt import create_access_token, create_refresh_token
from app.common.exceptions import InvalidCredentialsError
from app.core.config import settings
from app.db.dependencies import get_auth_service
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshResponse,
    RegisteredUserResponse,
    RegistrationRequest,
    RegistrationResponse,
)
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


@router.post(
    "/auth/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    tags=["Auth"],
)
async def login(
    payload: LoginRequest,
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginResponse:
    """Authenticate a user and issue authentication tokens."""

    user = await service.login(
        email=str(payload.email),
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

    return LoginResponse(
        user=RegisteredUserResponse.model_validate(user),
        access_token=access_token,
    )


@router.post(
    "/auth/refresh",
    response_model=RefreshResponse,
    status_code=status.HTTP_200_OK,
    tags=["Auth"],
)
async def refresh(
    service: Annotated[AuthService, Depends(get_auth_service)],
    refresh_token: Annotated[
        str | None,
        Cookie(alias=settings.refresh_cookie_name),
    ] = None,
) -> RefreshResponse:
    """Issue a new access token using the refresh-token cookie."""

    if refresh_token is None:
        raise InvalidCredentialsError("Invalid refresh token.")

    access_token = await service.refresh(refresh_token)

    return RefreshResponse(access_token=access_token)


@router.post(
    "/auth/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Auth"],
)
async def logout(response: Response) -> None:
    """Clear the refresh-token cookie and log out the user."""

    response.delete_cookie(
        key=settings.refresh_cookie_name,
        path=settings.refresh_cookie_path,
        secure=settings.refresh_cookie_secure,
        httponly=True,
        samesite=settings.refresh_cookie_samesite,
    )
