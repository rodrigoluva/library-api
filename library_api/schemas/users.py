from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, field_validator

from library_api.models.users import UserRole


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator('name', mode='before')
    @classmethod
    def captalize_name(cls, v):
        return v.title()

    @field_validator('password')
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 4:
            raise ValueError('Password must be at least 4 characters')
        return v


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

    @field_validator('name', mode='before')
    @classmethod
    def captalize_name(cls, v):
        return v.title()

    @field_validator('password')
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 4:
            raise ValueError('Password must be at least 4 characters')
        return v


class UserPublicSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime


class UserListPublicSchema(BaseModel):
    users: List[UserPublicSchema]
    offset: int
    limit: int
