from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import jwt
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import (
    AccessTokenClaims,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.auth.password import hash_password, verify_password
from app.common.exceptions import (
    AccountInactiveError,
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.core.config import settings
from app.db.models import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


class MockPostgresError(Exception):
    """Simulate a PostgreSQL error with constraint diagnostics."""

    def __init__(self, constraint_name: str) -> None:
        super().__init__("duplicate key value violates unique constraint")
        self.diag = SimpleNamespace(constraint_name=constraint_name)


@pytest.mark.anyio
async def test_register_creates_user_with_hashed_password(
    db_session: AsyncSession,
) -> None:
    # Arrange
    repository = UserRepository(db_session)
    service = AuthService(repository, db_session)

    email = "  student@example.com "
    full_name = "  Test Student  "
    password = "secure-password-123"

    # Act
    user = await service.register(
        email=email,
        full_name=full_name,
        password=password,
    )

    # Assert
    assert user.email == "student@example.com"
    assert user.full_name == "Test Student"
    assert user.is_active is True
    assert user.google_id is None

    assert user.password_hash is not None
    assert user.password_hash != password
    assert verify_password(password, user.password_hash)

    # Verify the user is queryable in the current transaction.
    result = await db_session.execute(select(User).where(User.email == "student@example.com"))
    persisted_user = result.scalar_one_or_none()

    assert persisted_user is not None
    assert persisted_user.id == user.id


@pytest.mark.anyio
async def test_register_raises_error_for_existing_email(
    db_session: AsyncSession,
    test_user: User,
) -> None:
    # Arrange
    repository = UserRepository(db_session)
    service = AuthService(repository, db_session)

    # Act & Assert
    with pytest.raises(EmailAlreadyRegisteredError) as exc_info:
        await service.register(
            email=test_user.email,
            full_name="Another User",
            password="another-password",
        )

    assert str(exc_info.value) == "An account with this email already exists."


@pytest.mark.anyio
async def test_register_translates_email_unique_constraint_violation(
    db_session: AsyncSession,
) -> None:
    # Arrange
    repository = UserRepository(db_session)
    service = AuthService(repository, db_session)

    original_error = MockPostgresError("uq_users_email")

    integrity_error = IntegrityError(
        statement="INSERT INTO users (...) VALUES (...)",
        params={},
        orig=original_error,
    )

    with patch.object(
        repository,
        "create",
        new_callable=AsyncMock,
        side_effect=integrity_error,
    ):
        # Act & Assert
        with pytest.raises(EmailAlreadyRegisteredError) as exc_info:
            await service.register(
                email="student@example.com",
                full_name="Test Student",
                password="secure-password-123",
            )

    assert str(exc_info.value) == "An account with this email already exists."


@pytest.mark.anyio
async def test_register_reraises_unrelated_integrity_error(
    db_session: AsyncSession,
) -> None:
    # Arrange
    repository = UserRepository(db_session)
    service = AuthService(repository, db_session)

    original_error = MockPostgresError("uq_users_google_id")
    integrity_error = IntegrityError(
        statement="INSERT INTO users (...) VALUES (...)",
        params={},
        orig=original_error,
    )

    with patch.object(
        repository,
        "create",
        new_callable=AsyncMock,
        side_effect=integrity_error,
    ):
        # Act & Assert
        with pytest.raises(IntegrityError) as exc_info:
            await service.register(
                email="student@example.com",
                full_name="Test Student",
                password="secure-password-123",
            )

    assert exc_info.value is integrity_error


@pytest.mark.anyio
async def test_login_with_valid_credentials(db_session):
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    password = "StrongPassword123!"
    password_hash = hash_password(password)

    user = await user_repository.create(
        email="student@example.com",
        full_name="Test Student",
        password_hash=password_hash,
    )

    authenticated_user = await auth_service.login(
        email="student@example.com",
        password=password,
    )

    assert authenticated_user.id == user.id
    assert authenticated_user.email == user.email


@pytest.mark.anyio
async def test_login_normalizes_email(db_session):
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    password = "StrongPassword123!"
    password_hash = hash_password(password)

    user = await user_repository.create(
        email="student@example.com",
        full_name="Test Student",
        password_hash=password_hash,
    )

    authenticated_user = await auth_service.login(
        email="  STUDENT@EXAMPLE.COM  ",
        password=password,
    )

    assert authenticated_user.id == user.id


@pytest.mark.anyio
async def test_login_rejects_incorrect_password(db_session):
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    await user_repository.create(
        email="student@example.com",
        full_name="Test Student",
        password_hash=hash_password("CorrectPassword123!"),
    )

    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            email="student@example.com",
            password="WrongPassword123!",
        )


@pytest.mark.anyio
async def test_login_rejects_nonexistent_email(db_session):
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            email="unknown@example.com",
            password="StrongPassword123!",
        )


@pytest.mark.anyio
async def test_login_rejects_google_only_account(db_session):
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    await user_repository.create(
        email="google@example.com",
        full_name="Google Student",
        password_hash=None,
    )

    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            email="google@example.com",
            password="StrongPassword123!",
        )


@pytest.mark.anyio
async def test_login_rejects_inactive_user(db_session):
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    user = await user_repository.create(
        email="inactive@example.com",
        full_name="Inactive Student",
        password_hash=hash_password("StrongPassword123!"),
    )

    user.is_active = False
    await db_session.flush()

    with pytest.raises(AccountInactiveError):
        await auth_service.login(
            email="inactive@example.com",
            password="StrongPassword123!",
        )


@pytest.mark.anyio
async def test_refresh_returns_new_access_token(
    db_session: AsyncSession,
) -> None:
    # Arrange
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    user = await user_repository.create(
        email="student@example.com",
        full_name="Test Student",
        password_hash=hash_password("StrongPassword123!"),
    )

    refresh_token = create_refresh_token(user.id)

    # Act
    access_token = await auth_service.refresh(refresh_token)

    # Assert
    access_claims = decode_token(access_token)

    assert isinstance(access_claims, AccessTokenClaims)
    assert access_claims.sub == user.id
    assert access_claims.type.value == "access"
    assert access_claims.email == user.email


@pytest.mark.anyio
async def test_refresh_rejects_access_token(
    db_session: AsyncSession,
) -> None:
    # Arrange
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    user = await user_repository.create(
        email="student@example.com",
        full_name="Test Student",
        password_hash=hash_password("StrongPassword123!"),
    )

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
    )

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(access_token)


@pytest.mark.anyio
async def test_refresh_rejects_nonexistent_user(
    db_session: AsyncSession,
) -> None:
    # Arrange
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    refresh_token = create_refresh_token(uuid4())

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(refresh_token)


@pytest.mark.anyio
async def test_refresh_rejects_inactive_user(
    db_session: AsyncSession,
) -> None:
    # Arrange
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    user = await user_repository.create(
        email="inactive@example.com",
        full_name="Inactive Student",
        password_hash=hash_password("StrongPassword123!"),
    )

    user.is_active = False
    await db_session.flush()

    refresh_token = create_refresh_token(user.id)

    # Act & Assert
    with pytest.raises(AccountInactiveError):
        await auth_service.refresh(refresh_token)


@pytest.mark.anyio
async def test_refresh_rejects_expired_token(
    db_session: AsyncSession,
) -> None:
    # Arrange
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    user = await user_repository.create(
        email="student@example.com",
        full_name="Test Student",
        password_hash=hash_password("StrongPassword123!"),
    )

    expired_time = datetime.now(timezone.utc) - timedelta(minutes=1)

    expired_refresh_token = jwt.encode(
        {
            "sub": str(user.id),
            "type": "refresh",
            "iat": int((expired_time - timedelta(minutes=5)).timestamp()),
            "exp": int(expired_time.timestamp()),
            "jti": str(uuid4()),
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(expired_refresh_token)


@pytest.mark.anyio
async def test_refresh_rejects_invalid_signature(
    db_session: AsyncSession,
) -> None:
    # Arrange
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    user = await user_repository.create(
        email="student@example.com",
        full_name="Test Student",
        password_hash=hash_password("StrongPassword123!"),
    )

    valid_refresh_token = create_refresh_token(user.id)

    token_payload = jwt.decode(
        valid_refresh_token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
        options={"verify_signature": False},
    )

    invalid_signature_token = jwt.encode(
        token_payload,
        "different-secret-that-is-at-least-32-bytes",
        algorithm=settings.jwt_algorithm,
    )

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(invalid_signature_token)


@pytest.mark.anyio
async def test_refresh_rejects_malformed_token(
    db_session: AsyncSession,
) -> None:
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository, db_session)

    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh("not-a-jwt")
