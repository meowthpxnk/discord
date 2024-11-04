import re
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, constr, field_validator


class JWTTokenTypeEnum(Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class UserAuthForm(BaseModel):
    username: str
    password: str

    @field_validator("username", "password")
    def non_empty_string(cls, value, field):
        # Check if the field is empty or contains only whitespace
        if not value.strip():
            raise ValueError(
                f"{field.field_name.capitalize()} cannot be empty or whitespace"
            )
        return value


class UserRegForm(BaseModel):
    # Username must be 3-50 characters long and can only contain letters, numbers, '_', '-', and '.'
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9_.-]+$",
        description="Username must be between 3 and 50 characters and may only include letters, numbers, '_', '-', and '.'",
    )

    # Password must be 8-100 characters and include at least one uppercase letter, one lowercase letter, one digit, and one special character
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password must be 8-100 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
    )

    @field_validator("password")
    def validate_password(cls, value):
        # Ensure the password contains at least one uppercase letter
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        # Ensure the password contains at least one lowercase letter
        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        # Ensure the password contains at least one digit
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")

        # Ensure the password contains at least one special character
        if not re.search(r"[!@#$%^&*()_+{}\[\]:;\"'|\\,.<>/?~-]", value):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return value


class User(BaseModel):
    username: str


class UserDataResponseModel(BaseModel):
    id: str
    username: str
    created_at: datetime


class TokenPayloadSchema(User):
    session_id: str


class TokenDataSchema(TokenPayloadSchema):
    exp: int
    type: JWTTokenTypeEnum


class ServerResponseModel(BaseModel):
    id: str
    title: str
    created_at: datetime


class ChatResponseModel(BaseModel):
    id: str
    title: str
    created_at: datetime


class MessageResponseModel(BaseModel):
    body: str
    user_id: str
    created_at: datetime


class ServerRequestForm(BaseModel):
    title: str = Field(
        ...,
        min_length=8,
        max_length=30,
        description="Title must be between 8 and 30 characters long",
    )


class MessageRequestForm(BaseModel):
    body: str
