from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.auth.jwt import create_access_token
from app.db.models.user import User


@pytest.mark.anyio
async def test_get_user_by_id(
    async_client: AsyncClient,
    test_user: User,
    override_get_db: None,
) -> None:
    access_token = create_access_token(
        user_id=test_user.id,
        email=test_user.email,
    )

    response = await async_client.get(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(test_user.id)
    assert data["is_active"] is True
    assert data["deleted_at"] is None
    assert data["created_at"] is not None


@pytest.mark.anyio
async def test_get_user_without_authentication(
    async_client: AsyncClient,
    test_user: User,
    override_get_db: None,
) -> None:
    response = await async_client.get(
        f"/api/v1/users/{test_user.id}",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.anyio
async def test_get_user_with_invalid_token(
    async_client: AsyncClient,
    test_user: User,
    override_get_db: None,
) -> None:
    response = await async_client.get(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.anyio
async def test_get_user_not_found(
    async_client: AsyncClient,
    test_user: User,
    override_get_db: None,
) -> None:
    user_id = uuid4()

    access_token = create_access_token(
        user_id=test_user.id,
        email=test_user.email,
    )

    response = await async_client.get(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_user_invalid_uuid(
    async_client: AsyncClient,
    test_user: User,
    override_get_db: None,
) -> None:
    access_token = create_access_token(
        user_id=test_user.id,
        email=test_user.email,
    )

    response = await async_client.get(
        "/api/v1/users/not-a-uuid",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_another_user_forbidden(
    async_client: AsyncClient,
    test_user: User,
    another_user: User,
    override_get_db: None,
) -> None:
    access_token = create_access_token(
        user_id=test_user.id,
        email=test_user.email,
    )

    response = await async_client.get(
        f"/api/v1/users/{another_user.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"
