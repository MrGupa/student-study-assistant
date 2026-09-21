from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

import jwt
from pydantic import BaseModel, ValidationError

from app.core.config import settings


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class BaseTokenClaims(BaseModel):
    sub: UUID
    iat: datetime
    exp: datetime
    jti: UUID


class AccessTokenClaims(BaseTokenClaims):
    type: Literal[TokenType.ACCESS]
    email: str


class RefreshTokenClaims(BaseTokenClaims):
    type: Literal[TokenType.REFRESH]


class JWTValidationError(Exception):
    """Raised when a JWT is invalid or cannot be validated."""


def _create_token(claims: AccessTokenClaims | RefreshTokenClaims) -> str:
    payload = claims.model_dump()
    payload["sub"] = str(claims.sub)
    payload["jti"] = str(claims.jti)
    payload["iat"] = int(claims.iat.timestamp())
    payload["exp"] = int(claims.exp.timestamp())
    payload["type"] = claims.type.value

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(user_id: UUID, email: str) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)
    claims = AccessTokenClaims(
        sub=user_id,
        iat=now,
        exp=expires_at,
        jti=uuid4(),
        type=TokenType.ACCESS,
        email=email,
    )
    return _create_token(claims)


def create_refresh_token(user_id: UUID) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=settings.refresh_token_expire_days)
    claims = RefreshTokenClaims(
        sub=user_id,
        iat=now,
        exp=expires_at,
        jti=uuid4(),
        type=TokenType.REFRESH,
    )
    return _create_token(claims)


def decode_token(token: str) -> AccessTokenClaims | RefreshTokenClaims:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError as exc:
        raise JWTValidationError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise JWTValidationError("Invalid token") from exc

    token_type = payload.get("type")

    try:
        if token_type == TokenType.ACCESS.value:
            return AccessTokenClaims.model_validate(payload)

        elif token_type == TokenType.REFRESH.value:
            return RefreshTokenClaims.model_validate(payload)

        else:
            raise JWTValidationError("Invalid token type")

    except ValidationError as exc:
        raise JWTValidationError("Invalid token claims") from exc
