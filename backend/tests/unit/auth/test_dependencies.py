from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

import app.auth.dependencies as auth_dependencies
from app.auth.jwt import (
    AccessTokenClaims,
    JWTValidationError,
    RefreshTokenClaims,
    TokenType,
)
from app.db.models import User


def make_access_claims() -> AccessTokenClaims:
    now = datetime.now(timezone.utc)
    return AccessTokenClaims(
        sub=uuid4(),
        iat=now,
        exp=now + timedelta(minutes=15),
        jti=uuid4(),
        type=TokenType.ACCESS,
        email="student@example.com",
    )


def make_credentials() -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="test-token",
    )


@pytest.mark.anyio
async def test_missing_credentials_returns_401() -> None:
    repository = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await auth_dependencies.get_current_user(
            credentials=None,
            repository=repository,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}
    repository.get_by_id.assert_not_awaited()


@pytest.mark.anyio
async def test_invalid_token_returns_401(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = AsyncMock()

    def raise_invalid_token(token: str) -> None:
        raise JWTValidationError("Invalid token")

    monkeypatch.setattr(
        auth_dependencies,
        "decode_token",
        raise_invalid_token,
    )

    with pytest.raises(HTTPException) as exc_info:
        await auth_dependencies.get_current_user(
            credentials=make_credentials(),
            repository=repository,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}
    repository.get_by_id.assert_not_awaited()


@pytest.mark.anyio
async def test_refresh_token_returns_401(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = AsyncMock()
    now = datetime.now(timezone.utc)

    claims = RefreshTokenClaims(
        sub=uuid4(),
        iat=now,
        exp=now + timedelta(days=30),
        jti=uuid4(),
        type=TokenType.REFRESH,
    )

    monkeypatch.setattr(
        auth_dependencies,
        "decode_token",
        lambda token: claims,
    )

    with pytest.raises(HTTPException) as exc_info:
        await auth_dependencies.get_current_user(
            credentials=make_credentials(),
            repository=repository,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}
    repository.get_by_id.assert_not_awaited()


@pytest.mark.anyio
async def test_nonexistent_user_returns_401(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = AsyncMock()
    claims = make_access_claims()
    repository.get_by_id.return_value = None

    monkeypatch.setattr(
        auth_dependencies,
        "decode_token",
        lambda token: claims,
    )

    with pytest.raises(HTTPException) as exc_info:
        await auth_dependencies.get_current_user(
            credentials=make_credentials(),
            repository=repository,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}
    repository.get_by_id.assert_awaited_once_with(claims.sub)


@pytest.mark.anyio
async def test_soft_deleted_user_returns_401(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = AsyncMock()
    claims = make_access_claims()

    user = User(
        id=claims.sub,
        email="student@example.com",
        full_name="Test Student",
        is_active=True,
        deleted_at=datetime.now(timezone.utc),
    )
    repository.get_by_id.return_value = user

    monkeypatch.setattr(
        auth_dependencies,
        "decode_token",
        lambda token: claims,
    )

    with pytest.raises(HTTPException) as exc_info:
        await auth_dependencies.get_current_user(
            credentials=make_credentials(),
            repository=repository,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.anyio
async def test_inactive_user_returns_403(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = AsyncMock()
    claims = make_access_claims()

    user = User(
        id=claims.sub,
        email="student@example.com",
        full_name="Test Student",
        is_active=False,
    )
    repository.get_by_id.return_value = user

    monkeypatch.setattr(
        auth_dependencies,
        "decode_token",
        lambda token: claims,
    )

    with pytest.raises(HTTPException) as exc_info:
        await auth_dependencies.get_current_user(
            credentials=make_credentials(),
            repository=repository,
        )

    assert exc_info.value.status_code == 403


@pytest.mark.anyio
async def test_active_user_is_returned(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = AsyncMock()
    claims = make_access_claims()

    user = User(
        id=claims.sub,
        email="student@example.com",
        full_name="Test Student",
        is_active=True,
    )
    repository.get_by_id.return_value = user

    monkeypatch.setattr(
        auth_dependencies,
        "decode_token",
        lambda token: claims,
    )

    result = await auth_dependencies.get_current_user(
        credentials=make_credentials(),
        repository=repository,
    )

    assert result is user
    repository.get_by_id.assert_awaited_once_with(claims.sub)
