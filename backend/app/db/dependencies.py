from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    """Provide a UserRepository instance."""

    return UserRepository(session)


def get_user_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> UserService:
    return UserService(repository)
