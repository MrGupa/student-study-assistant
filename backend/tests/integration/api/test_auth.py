import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.password import verify_password
from app.core.config import settings
from app.db.models.user import User


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

    assert user["id"] is not None
    assert user["email"] == payload["email"]
    assert user["full_name"] == payload["full_name"]
    assert user["is_active"] is True

    assert "password" not in data
    assert "password_hash" not in data

    assert data["access_token"]
    assert data["token_type"] == "bearer"

    # Refresh token must not be exposed in the JSON body.
    assert "refresh_token" not in data

    # Verify refresh token is issued through the cookie.
    set_cookie = response.headers["set-cookie"]

    assert settings.refresh_cookie_name in set_cookie
    assert "HttpOnly" in set_cookie
    assert f"Path={settings.refresh_cookie_path}" in set_cookie
    assert f"SameSite={settings.refresh_cookie_samesite}" in set_cookie

    if settings.refresh_cookie_secure:
        assert "Secure" in set_cookie


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

    # First registration should succeed.
    first_response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )
    assert first_response.status_code == 201

    # Registering with the same email should fail.
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
    payload = {
        "email": "invalid-email",
        "full_name": "Test User",
        "password": "SecurePassword123!",
    }

    response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "email"] for error in errors)


@pytest.mark.anyio
async def test_registration_with_weak_password(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "weak",
    }

    response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "password"] for error in errors)


@pytest.mark.anyio
async def test_registration_with_missing_email(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    payload = {
        "full_name": "Test User",
        "password": "SecurePassword123!",
    }

    response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "email"] for error in errors)


@pytest.mark.anyio
async def test_email_normalization_during_registration(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    payload = {
        "email": "TEST@example.com",
        "full_name": "Test User",
        "password": "SecurePassword123!",
    }

    response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()
    assert data["user"]["email"] == "test@example.com"


@pytest.mark.anyio
async def test_full_name_normalization_during_registration(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    payload = {
        "email": "test@example.com",
        "full_name": "  Test User  ",
        "password": "SecurePassword123!",
    }

    response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()
    assert data["user"]["full_name"] == "Test User"


@pytest.mark.anyio
async def test_password_stored_as_hash(
    async_client: AsyncClient,
    override_get_db: None,
    db_session: AsyncSession,
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

    result = await db_session.execute(select(User).where(User.email == payload["email"]))
    user = result.scalar_one()

    assert user.password_hash is not None
    assert user.password_hash != payload["password"]
    assert verify_password(payload["password"], user.password_hash)


@pytest.mark.anyio
async def test_refresh_token_cookie_attributes(
    async_client: AsyncClient,
    override_get_db: None,
) -> None:
    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "SecurePassword123!",
    }

    # Registration issues the refresh-token cookie.
    response = await async_client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == 201

    set_cookie = response.headers["set-cookie"]

    assert settings.refresh_cookie_name in set_cookie
    assert "HttpOnly" in set_cookie
    assert f"Path={settings.refresh_cookie_path}" in set_cookie
    assert f"SameSite={settings.refresh_cookie_samesite}" in set_cookie

    if settings.refresh_cookie_secure:
        assert "Secure" in set_cookie
