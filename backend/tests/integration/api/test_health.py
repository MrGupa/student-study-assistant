import pytest


@pytest.mark.anyio
async def test_health_check(async_client) -> None:
    response = await async_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
