from uuid import UUID

import pytest
from pydantic import ValidationError

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisteredUserResponse,
    RegistrationRequest,
    RegistrationResponse,
)


def test_registration_request_normalizes_email_and_name() -> None:
    request = RegistrationRequest(
        email="  Student@Example.com ",
        full_name="  Gaurav Sharma  ",
        password="  valid-password-123  ",
    )

    assert request.email == "student@example.com"
    assert request.full_name == "Gaurav Sharma"
    assert request.password == "  valid-password-123  "


@pytest.mark.parametrize(
    "email",
    ["not-an-email", "", "student@"],
)
def test_registration_request_rejects_invalid_email(email: str) -> None:
    with pytest.raises(ValidationError):
        RegistrationRequest(
            email=email,
            full_name="Gaurav Sharma",
            password="valid-password-123",
        )


@pytest.mark.parametrize(
    "full_name",
    ["", "   ", "x" * 256],
)
def test_registration_request_rejects_invalid_full_name(
    full_name: str,
) -> None:
    with pytest.raises(ValidationError):
        RegistrationRequest(
            email="student@example.com",
            full_name=full_name,
            password="valid-password-123",
        )


@pytest.mark.parametrize(
    "password",
    ["short", "x" * 129],
)
def test_registration_request_rejects_password_outside_length(
    password: str,
) -> None:
    with pytest.raises(ValidationError):
        RegistrationRequest(
            email="student@example.com",
            full_name="Gaurav Sharma",
            password=password,
        )


def test_registration_response_excludes_internal_user_fields() -> None:
    response = RegistrationResponse(
        user=RegisteredUserResponse(
            id=UUID("a9a2e0a2-cae3-4db7-ae04-735b0d4e80e4"),
            email="student@example.com",
            full_name="Gaurav Patil",
            is_active=True,
        ),
        access_token="access-token",
    )

    response_data = response.model_dump()

    assert set(response_data["user"].keys()) == {
        "id",
        "email",
        "full_name",
        "is_active",
    }
    assert response_data["token_type"] == "bearer"


def test_login_request_normalizes_email_and_preserves_password() -> None:
    request = LoginRequest(
        email="  Student@Example.com ",
        password="  valid-password-123  ",
    )

    assert request.email == "student@example.com"
    assert request.password == "  valid-password-123  "


@pytest.mark.parametrize(
    "email",
    ["not-an-email", "", "student@"],
)
def test_login_request_rejects_invalid_email(email: str) -> None:
    with pytest.raises(ValidationError):
        LoginRequest(
            email=email,
            password="valid-password-123",
        )


@pytest.mark.parametrize(
    "password",
    ["short", "x" * 129],
)
def test_login_request_rejects_password_outside_length(
    password: str,
) -> None:
    with pytest.raises(ValidationError):
        LoginRequest(
            email="student@example.com",
            password=password,
        )


@pytest.mark.parametrize(
    "missing_field",
    ["email", "password"],
)
def test_login_request_rejects_missing_required_fields(
    missing_field: str,
) -> None:
    payload = {
        "email": "student@example.com",
        "password": "valid-password-123",
    }
    payload.pop(missing_field)

    with pytest.raises(ValidationError):
        LoginRequest(**payload)


def test_login_response_excludes_internal_user_fields() -> None:
    response = LoginResponse(
        user=RegisteredUserResponse(
            id=UUID("a9a2e0a2-cae3-4db7-ae04-735b0d4e80e4"),
            email="student@example.com",
            full_name="Gaurav Patil",
            is_active=True,
        ),
        access_token="access-token",
    )

    response_data = response.model_dump()

    assert "password_hash" not in response_data["user"]
    assert "google_id" not in response_data["user"]
    assert response_data["token_type"] == "bearer"
