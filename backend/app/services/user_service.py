from app.repositories.user_repository import UserRepository


class UserService:
    """Business logic for users."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

