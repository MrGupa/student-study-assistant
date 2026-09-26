from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import (
    AccessTokenClaims,
    JWTValidationError,
    create_access_token,
    decode_token,
)
from app.auth.password import hash_password, verify_password
from app.common.exceptions import (
    AccountInactiveError,
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.db.models import User
from app.repositories.user_repository import UserRepository


class AuthService:
    """Business logic for authentication."""

    def __init__(
        self,
        repository: UserRepository,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._session = session

    async def register(
        self,
        *,
        email: str,
        full_name: str,
        password: str,
    ) -> User:
        """Register a new user with email and password."""

        normalized_email = email.strip().lower()
        normalized_full_name = full_name.strip()

        existing_user = await self._repository.get_by_email(normalized_email)
        if existing_user is not None:
            raise EmailAlreadyRegisteredError("An account with this email already exists.")

        password_hash = hash_password(password)

        try:
            user = await self._repository.create(
                email=normalized_email,
                full_name=normalized_full_name,
                password_hash=password_hash,
            )
            await self._session.commit()

        except IntegrityError as exc:
            await self._session.rollback()

            original_error = exc.orig
            diagnostics = getattr(original_error, "diag", None)
            constraint_name = getattr(diagnostics, "constraint_name", None)

            if constraint_name == "uq_users_email":
                raise EmailAlreadyRegisteredError(
                    "An account with this email already exists."
                ) from exc

            raise

        except Exception:
            await self._session.rollback()
            raise

        return user

    async def login(
        self,
        *,
        email: str,
        password: str,
    ) -> User:
        """Authenticate a user with email and password."""

        normalized_email = email.strip().lower()
        user = await self._repository.get_by_email(normalized_email)

        if user is None or user.password_hash is None:
            raise InvalidCredentialsError("Invalid email or password.")

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password.")

        if not user.is_active:
            raise AccountInactiveError("Inactive user.")

        return user

    async def refresh(self, refresh_token: str) -> str:
        """Create a new access token from a valid refresh token."""

        try:
            claims = decode_token(refresh_token)
        except JWTValidationError as exc:
            raise InvalidCredentialsError("Invalid refresh token.") from exc

        if isinstance(claims, AccessTokenClaims):
            raise InvalidCredentialsError("Invalid refresh token.")

        user = await self._repository.get_by_id(claims.sub)

        if user is None:
            raise InvalidCredentialsError("Invalid refresh token.")

        if not user.is_active:
            raise AccountInactiveError("Inactive user.")

        return create_access_token(
            user_id=user.id,
            email=user.email,
        )
