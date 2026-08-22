from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from app.core.config import settings

test_engine = create_async_engine(
    settings.test_database_url,
    echo=settings.debug,
)


def create_test_db_dependency(session: AsyncSession):
    async def test_get_db():
        yield session

    return test_get_db
