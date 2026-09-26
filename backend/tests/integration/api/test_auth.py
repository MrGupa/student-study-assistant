from uuid import uuid4

import jwt
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import create_access_token, create_refresh_token
from app.auth.password import hash_password, verify_password
from app.core.config import settings
from app.db.models.user import User


def assert_refresh_cookie(response) -> None:
    """Verify refresh-token cookie security attributes."""
    set_cookie = response.headers["set-cookie"]

    assert settings.refresh_cookie_name in set_cookie
    assert "HttpOnly" in set_cookie
    assert f"Path={settings.refresh_cookie_path}" in set_cookie
    assert f"SameSite={settings.refresh_cookie_samesite}" in set_cookie

    if settings.refresh_cookie_secure:
        assert "Secure" in set_cookie


def assert_public_user_response(user: dict) -> None:
    """Ensure only public user fields are returned."""
    assert set(user.keys()) == {
        "id",
        "email",
        "full_name",
        "is_active",
    }

    assert user["id"]
    assert user["is_active"] is True


def assert_invalid_credentials_response(response) -> None:
    """Verify the generic invalid-credentials response."""
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    assert response.headers["www-authenticate"] == "Bearer"


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_successful_registration(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "SecurePassword123!",
    }

    response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()
    user = data["user"]

    assert_public_user_response(user)

    assert user["email"] == payload["email"]
    assert user["full_name"] == payload["full_name"]

    assert data["access_token"]
    assert data["token_type"] == "bearer"

    # Sensitive credentials must not be exposed in the JSON response.
    assert "password" not in data
    assert "password_hash" not in data
    assert "refresh_token" not in data

    assert_refresh_cookie(response)


@pytest.mark.anyio
async def test_registration_with_existing_email(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "SecurePassword123!",
    }

    first_response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already exists"


@pytest.mark.anyio
async def test_registration_with_invalid_email(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "invalid-email",
            "full_name": "Test User",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "email"] for error in errors)


@pytest.mark.anyio
async def test_registration_with_weak_password(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "weak",
        },
    )

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "password"] for error in errors)


@pytest.mark.anyio
async def test_registration_with_missing_email(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "email"] for error in errors)


@pytest.mark.anyio
async def test_email_normalization_during_registration(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "TEST@example.com",
            "full_name": "Test User",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 201
    assert response.json()["user"]["email"] == "test@example.com"


@pytest.mark.anyio
async def test_full_name_normalization_during_registration(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "  Test User  ",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 201
    assert response.json()["user"]["full_name"] == "Test User"


@pytest.mark.anyio
async def test_password_stored_as_hash(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
) -> None:
    password = "SecurePassword123!"

    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": password,
        },
    )

    assert response.status_code == 201

    result = await db_session.execute(select(User).where(User.email == "test@example.com"))
    user = result.scalar_one()

    assert user.password_hash is not None
    assert user.password_hash != password
    assert verify_password(password, user.password_hash)


@pytest.mark.anyio
async def test_registration_refresh_cookie_attributes(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 201
    assert_refresh_cookie(response)


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_nonexistent_user_login(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "AnyPassword123!",
        },
    )

    assert_invalid_credentials_response(response)


@pytest.mark.anyio
async def test_google_only_account_login(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
) -> None:
    user = User(
        email="googleuser@example.com",
        full_name="Google User",
        password_hash=None,
        google_id="google-sub-123",
    )

    db_session.add(user)
    await db_session.flush()

    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "googleuser@example.com",
            "password": "GooglePassword123!",
        },
    )

    assert_invalid_credentials_response(response)


@pytest.mark.anyio
async def test_inactive_user_login(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
) -> None:
    user = User(
        email="inactiveuser@example.com",
        full_name="Inactive User",
        password_hash=hash_password("InactivePassword123!"),
        is_active=False,
    )

    db_session.add(user)
    await db_session.flush()

    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "inactiveuser@example.com",
            "password": "InactivePassword123!",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Inactive account"


@pytest.mark.anyio
async def test_login_with_invalid_email(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalid-email",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_with_missing_password(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
        },
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_successful_login(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
) -> None:
    password = "SecurePassword123!"

    user = User(
        email="loginuser@example.com",
        full_name="Login User",
        password_hash=hash_password(password),
    )

    db_session.add(user)
    await db_session.flush()

    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "loginuser@example.com",
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()
    response_user = data["user"]

    assert_public_user_response(response_user)

    assert response_user["email"] == "loginuser@example.com"
    assert response_user["full_name"] == "Login User"

    assert data["access_token"]
    assert data["token_type"] == "bearer"

    # Sensitive credentials must not be exposed in the JSON response.
    assert "password" not in response_user
    assert "password_hash" not in response_user
    assert "refresh_token" not in data

    assert_refresh_cookie(response)


@pytest.mark.anyio
async def test_login_with_incorrect_password(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
) -> None:
    user = User(
        email="loginuser@example.com",
        full_name="Login User",
        password_hash=hash_password("CorrectPassword123!"),
    )

    db_session.add(user)
    await db_session.flush()

    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "loginuser@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert_invalid_credentials_response(response)


@pytest.mark.anyio
async def test_login_refresh_cookie_attributes(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
) -> None:
    password = "SecurePassword123!"

    user = User(
        email="cookieuser@example.com",
        full_name="Cookie User",
        password_hash=hash_password(password),
    )

    db_session.add(user)
    await db_session.flush()

    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "cookieuser@example.com",
            "password": password,
        },
    )

    assert response.status_code == 200
    assert_refresh_cookie(response)


# ---------------------------------------------------------------------------
# Refresh
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_successful_token_refresh(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
) -> None:
    user = User(
        email="refreshuser@example.com",
        full_name="Refresh User",
        password_hash=hash_password("RefreshPassword123!"),
    )
    db_session.add(user)
    await db_session.flush()

    refresh_token = create_refresh_token(user.id)

    async_client.cookies.set(
        settings.refresh_cookie_name,
        refresh_token,
    )

    response = await async_client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"]
    assert data["token_type"] == "bearer"

    assert set(data.keys()) == {
        "access_token",
        "token_type",
    }

    assert "refresh_token" not in data
    assert "user" not in data


@pytest.mark.anyio
async def test_refresh_without_cookie(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    response = await async_client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.anyio
async def test_refresh_with_invalid_token(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    async_client.cookies.set(
        settings.refresh_cookie_name,
        "not-a-valid-jwt",
    )

    response = await async_client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.anyio
async def test_refresh_with_access_token(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
) -> None:
    user = User(
        email="access-token-refresh@example.com",
        full_name="Access Token User",
        password_hash=hash_password("AccessPassword123!"),
    )
    db_session.add(user)
    await db_session.flush()

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
    )

    async_client.cookies.set(
        settings.refresh_cookie_name,
        access_token,
    )

    response = await async_client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.anyio
async def test_refresh_with_inactive_user(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
) -> None:
    user = User(
        email="inactive-refresh@example.com",
        full_name="Inactive Refresh User",
        password_hash=hash_password("InactivePassword123!"),
        is_active=False,
    )
    db_session.add(user)
    await db_session.flush()

    refresh_token = create_refresh_token(user.id)

    async_client.cookies.set(
        settings.refresh_cookie_name,
        refresh_token,
    )

    response = await async_client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Inactive account"


@pytest.mark.anyio
async def test_refresh_with_nonexistent_user(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    refresh_token = create_refresh_token(uuid4())

    async_client.cookies.set(
        settings.refresh_cookie_name,
        refresh_token,
    )

    response = await async_client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.anyio
async def test_refresh_with_expired_token(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    expired_token = jwt.encode(
        {
            "sub": str(uuid4()),
            "iat": 1,
            "exp": 2,
            "jti": str(uuid4()),
            "type": "refresh",
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    async_client.cookies.set(
        settings.refresh_cookie_name,
        expired_token,
    )

    response = await async_client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.anyio
async def test_refresh_with_invalid_signature(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    token = jwt.encode(
        {
            "sub": str(uuid4()),
            "iat": 1,
            "exp": 4_102_444_800,
            "jti": str(uuid4()),
            "type": "refresh",
        },
        "different-secret-that-is-at-least-32-bytes",
        algorithm=settings.jwt_algorithm,
    )

    async_client.cookies.set(
        settings.refresh_cookie_name,
        token,
    )

    response = await async_client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    assert response.headers["www-authenticate"] == "Bearer"
