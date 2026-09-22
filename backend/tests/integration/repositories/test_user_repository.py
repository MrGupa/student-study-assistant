from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository


@pytest.mark.anyio
async def test_create_user_returns_persisted_user(
    db_session: AsyncSession,
) -> None:
    # Arrange
    repository = UserRepository(db_session)

    email = "test@example.com"
    full_name = "Test User"
    password_hash = "test-password-hash"

    # Act
    created_user = await repository.create(
        email=email,
        full_name=full_name,
        password_hash=password_hash,
    )

    # Assert
    assert isinstance(created_user.id, UUID)
    assert created_user.email == email
    assert created_user.full_name == full_name
    assert created_user.password_hash == password_hash
    assert created_user.is_active is True
    assert created_user.google_id is None

    # Verify the user can be retrieved within the same transaction.
    retrieved_user = await repository.get_by_id(created_user.id)

    assert retrieved_user is not None
    assert retrieved_user.email == email
    assert retrieved_user.full_name == full_name
