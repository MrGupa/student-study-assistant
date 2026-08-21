from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

test_engine = create_async_engine(
    settings.test_database_url,
    echo=settings.debug,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def test_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for a single request."""

    async with TestSessionLocal() as session:
        yield session
