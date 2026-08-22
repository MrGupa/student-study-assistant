from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.db.models.user import User


@pytest.mark.anyio
async def test_get_user_by_id(
    async_client: AsyncClient, test_user: User, override_get_db: None
) -> None:
    response = await async_client.get(f"/api/v1/users/{test_user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_user.id)
    assert data["is_active"] is True
    assert data["deleted_at"] is None
    assert data["created_at"] is not None


@pytest.mark.anyio
async def test_get_user_not_found(async_client: AsyncClient, override_get_db: None) -> None:
    user_id = uuid4()
    response = await async_client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_user_invalid_uuid(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/users/not-a-uuid")

    assert response.status_code == 422
