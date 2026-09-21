from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
import pytest
from pydantic import ValidationError

from app.auth.jwt import (
    AccessTokenClaims,
    JWTValidationError,
    RefreshTokenClaims,
    TokenType,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.config import settings


def test_access_token_claims_accept_valid_data() -> None:
    claims = AccessTokenClaims(
        sub=uuid4(),
        iat=datetime.now(timezone.utc),
        exp=datetime.now(timezone.utc),
        jti=uuid4(),
        type=TokenType.ACCESS,
        email="student@example.com",
    )

    assert claims.type == TokenType.ACCESS
    assert claims.email == "student@example.com"


def test_refresh_token_claims_accept_valid_data() -> None:
    claims = RefreshTokenClaims(
        sub=uuid4(),
        iat=datetime.now(timezone.utc),
        exp=datetime.now(timezone.utc),
        jti=uuid4(),
        type=TokenType.REFRESH,
    )

    assert claims.type == TokenType.REFRESH


def test_access_token_claims_require_email() -> None:
    with pytest.raises(ValidationError):
        AccessTokenClaims(
            sub=uuid4(),
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc),
            jti=uuid4(),
            type=TokenType.ACCESS,
            # mypy: email is intentionally omitted for validation testing
        )  # type: ignore[call-arg]


def test_access_token_claims_reject_refresh_type() -> None:
    with pytest.raises(ValidationError):
        AccessTokenClaims(
            sub=uuid4(),
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc),
            jti=uuid4(),
            type=TokenType.REFRESH,  # type: ignore[arg-type]
            email="student@example.com",
        )


def test_refresh_token_claims_reject_access_type() -> None:
    with pytest.raises(ValidationError):
        RefreshTokenClaims(
            sub=uuid4(),
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc),
            jti=uuid4(),
            type=TokenType.ACCESS,  # type: ignore[arg-type]
        )


def test_create_access_token_returns_jwt_string() -> None:
    user_id = uuid4()

    token = create_access_token(
        user_id=user_id,
        email="student@example.com",
    )

    assert isinstance(token, str)


def test_create_access_token_returns_decodable_jwt() -> None:
    user_id = uuid4()

    token = create_access_token(
        user_id=user_id,
        email="student@example.com",
    )

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["type"] == TokenType.ACCESS.value


def test_create_access_token_contains_expected_identity_claims() -> None:
    user_id = uuid4()
    email = "student@example.com"

    token = create_access_token(
        user_id=user_id,
        email=email,
    )

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == str(user_id)
    assert payload["email"] == email
    assert payload["type"] == TokenType.ACCESS.value


def test_create_access_token_has_configured_expiration() -> None:
    token = create_access_token(
        user_id=uuid4(),
        email="student@example.com",
    )

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    expected_lifetime = settings.access_token_expire_minutes * 60

    assert payload["exp"] - payload["iat"] == expected_lifetime


def test_create_access_token_generates_unique_jti() -> None:
    user_id = uuid4()
    email = "student@example.com"

    token_one = create_access_token(
        user_id=user_id,
        email=email,
    )
    token_two = create_access_token(
        user_id=user_id,
        email=email,
    )

    payload_one = jwt.decode(
        token_one,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
    payload_two = jwt.decode(
        token_two,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload_one["jti"] != payload_two["jti"]


def test_create_refresh_token_returns_jwt_string() -> None:
    user_id = uuid4()

    token = create_refresh_token(
        user_id=user_id,
    )

    assert isinstance(token, str)


def test_create_refresh_token_returns_decodable_jwt() -> None:
    user_id = uuid4()

    token = create_refresh_token(
        user_id=user_id,
    )

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
    assert payload["type"] == TokenType.REFRESH.value


def test_create_refresh_token_contains_expected_identity_claims() -> None:
    user_id = uuid4()

    token = create_refresh_token(
        user_id=user_id,
    )

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == str(user_id)
    assert payload["type"] == TokenType.REFRESH.value


def test_create_refresh_token_has_configured_expiration() -> None:
    token = create_refresh_token(
        user_id=uuid4(),
    )

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    expected_lifetime = settings.refresh_token_expire_days * 60 * 60 * 24

    assert payload["exp"] - payload["iat"] == expected_lifetime


def test_create_refresh_token_generates_unique_jti() -> None:
    user_id = uuid4()

    token_one = create_refresh_token(
        user_id=user_id,
    )
    token_two = create_refresh_token(
        user_id=user_id,
    )

    payload_one = jwt.decode(
        token_one,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
    payload_two = jwt.decode(
        token_two,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload_one["jti"] != payload_two["jti"]


def test_valid_access_token_returns_access_token_claims() -> None:
    user_id = uuid4()
    email = "student@example.com"

    token = create_access_token(user_id=user_id, email=email)

    claims = decode_token(token)

    assert isinstance(claims, AccessTokenClaims)
    assert claims.sub == user_id
    assert claims.email == email


def test_valid_refresh_token_returns_refresh_token_claims() -> None:
    user_id = uuid4()

    token = create_refresh_token(user_id=user_id)

    claims = decode_token(token)

    assert isinstance(claims, RefreshTokenClaims)
    assert claims.sub == user_id


def test_wrong_signing_secret_raises_jwt_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    user_id = uuid4()
    email = "student@example.com"

    token = create_access_token(user_id=user_id, email=email)

    monkeypatch.setattr(settings, "jwt_secret", "incorrect_secret_for_jwt_testing_32")

    with pytest.raises(JWTValidationError):
        decode_token(token)


def test_expired_token_raises_jwt_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    user_id = uuid4()
    email = "student@example.com"

    monkeypatch.setattr(settings, "access_token_expire_minutes", -1)

    token = create_access_token(user_id=user_id, email=email)

    with pytest.raises(JWTValidationError):
        decode_token(token)


def test_unknown_token_type_raises_jwt_validation_error() -> None:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(uuid4()),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=5)).timestamp()),
        "jti": str(uuid4()),
        "type": "unknown_type",
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(JWTValidationError):
        decode_token(token)


def test_missing_required_claim_raises_jwt_validation_error() -> None:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(uuid4()),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=5)).timestamp()),
        "jti": str(uuid4()),
        "type": TokenType.ACCESS.value,
        # Required access-token claim "email" is intentionally missing.
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(JWTValidationError):
        decode_token(token)
