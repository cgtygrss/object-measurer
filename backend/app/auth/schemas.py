"""Auth request/response schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ─── Request Schemas ───────────────────────────────────────────

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str | None = Field(None, max_length=100)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


# ─── Response Schemas ──────────────────────────────────────────

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    display_name: str | None
    unit_preference: str
    is_premium: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserUpdateRequest(BaseModel):
    display_name: str | None = None
    unit_preference: str | None = Field(None, pattern="^(cm|mm|in)$")
