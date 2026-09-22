from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from tests.integration.database import test_engine


@pytest.mark.anyio
async def test_transaction_rollback(db_session: AsyncSession) -> None:
    # Arrange
    email = f"{uuid4()}@example.com"

    user = User(
        email=email,
        full_name="Test User",
        password_hash="test-password-hash",
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.commit()

    result = await db_session.execute(select(User).where(User.email == email))
    assert result.scalar_one_or_none() is not None

    async with AsyncSession(bind=test_engine) as verification_session:
        result = await verification_session.execute(select(User).where(User.email == email))

        assert result.scalar_one_or_none() is None
