from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.jwt import (
    AccessTokenClaims,
    JWTValidationError,
    decode_token,
)
from app.db.dependencies import get_user_repository
from app.db.models import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> User:
    """Validate bearer access token and return the active, non-deleted user."""

    if credentials is None:
        raise _unauthorized()

    try:
        claims = decode_token(credentials.credentials)
    except JWTValidationError as exc:
        raise _unauthorized() from exc

    if not isinstance(claims, AccessTokenClaims):
        raise _unauthorized()

    user = await repository.get_by_id(claims.sub)

    if user is None or user.deleted_at is not None:
        raise _unauthorized()

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user
