from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator


class AuthorSchema(BaseModel):
    name: str
    bio: Optional[str] = None
    birthdate: Optional[date] = None

    @field_validator('name', mode='before')
    @classmethod
    def captalize_name(cls, v):
        return v.title()


class AuthorUpdateSchema(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    birthdate: Optional[date] = None

    @field_validator('name', mode='before')
    @classmethod
    def captalize_name(cls, v):
        return v.title()


class AuthorPublicSchema(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None
    birthdate: Optional[date] = None
    created_at: datetime
    updated_at: datetime


class AuthorRelationshipPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class AuthorListPublicSchema(BaseModel):
    authors: List[AuthorPublicSchema]
    offset: int
    limit: int
