from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, field_validator

from library_api.schemas.authors import AuthorRelationshipPublicSchema


class BookSchema(BaseModel):
    title: str
    isbn: str
    published_date: Optional[date]
    author_id: int

    @field_validator('title')
    @classmethod
    def title_max_length(cls, v):
        if len(v.strip()) > 100:
            raise ValueError('The title cannot exceed 100 characters')
        return v.strip()


class BookUpdateSchema(BaseModel):
    title: Optional[str]
    isbn: Optional[str]
    published_date: Optional[date]
    author_id: Optional[int]

    @field_validator('title')
    @classmethod
    def title_max_length(cls, v):
        if len(v.strip()) > 100:
            raise ValueError('The title cannot exceed 100 characters')
        return v.strip()


class BookPublicSchema(BaseModel):
    id: int
    title: str
    author_id: int
    isbn: str
    published_date: Optional[date]
    created_at: datetime
    updated_at: datetime


class BookRelationshipPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    author: AuthorRelationshipPublicSchema
    isbn: str
    published_date: Optional[date]
    created_at: datetime
    updated_at: datetime


class BookRelationshipListPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    author: AuthorRelationshipPublicSchema
    isbn: str
    available_copies: Optional[int]
    published_date: Optional[date]
    created_at: datetime
    updated_at: datetime


class BookListPublicSchema(BaseModel):
    books: List[BookRelationshipListPublicSchema]
    offset: int
    limit: int