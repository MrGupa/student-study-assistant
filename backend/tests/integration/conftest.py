from collections.abc import AsyncIterator, Generator

import pytest
from httpx import ASGITransport, AsyncClient

from app.db.dependencies import get_db
from app.main import app
from tests.integration.database import test_get_db


@pytest.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def override_get_db() -> Generator[None, None, None]:
    app.dependency_overrides[get_db] = test_get_db
    yield
    app.dependency_overrides.pop(get_db, None)
