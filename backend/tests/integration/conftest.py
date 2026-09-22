from collections.abc import AsyncIterator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.db.models.user import User
from app.main import app
from tests.integration.database import create_test_db_dependency, test_engine


@pytest.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def override_get_db(db_session: AsyncSession) -> Generator[None, None, None]:
    test_db_dependency = create_test_db_dependency(db_session)
    app.dependency_overrides[get_db] = test_db_dependency
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    async with test_engine.connect() as conn:
        transaction = await conn.begin()

        async with AsyncSession(bind=conn, join_transaction_mode="create_savepoint") as session:
            try:
                yield session
            finally:
                await transaction.rollback()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    user = User(
        email="testuser@example.com",
        full_name="Test User",
    )

    db_session.add(user)
    await db_session.flush()

    return user
