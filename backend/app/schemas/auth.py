from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegistrationRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=12, max_length=128)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("full_name", mode="before")
    @classmethod
    def normalize_full_name(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value


class RegisteredUserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    is_active: bool


class RegistrationResponse(BaseModel):
    user: RegisteredUserResponse
    access_token: str
    token_type: Literal["bearer"] = "bearer"
