from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UserRepository:
    """Repository for user persistence operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a user by ID."""

        statement = select(User).where(User.id == user_id)
        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email."""

        statement = select(User).where(User.email == email)
        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def create(self, *, email: str, full_name: str, password_hash: str) -> User:
        """Create and persist a user."""

        user = User(
            email=email,
            full_name=full_name,
            password_hash=password_hash,
        )

        self._session.add(user)
        await self._session.flush()

        return user
