from uuid import UUID

from app.common.exceptions import UserNotFoundError
from app.db.models import User
from app.repositories.user_repository import UserRepository


class UserService:
    """Business logic for users."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def get_by_id(self, user_id: UUID) -> User:
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError("User not found")

        return user
