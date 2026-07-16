from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


from library_api.models.books import BookStatus
from library_api.schemas.books import (
    BookRelationshipPublicSchema,
)


class BookCopyCreateSchema(BaseModel):
    quantity: int = Field(default=1, gt=0, le=10, description='Number of book copies')


class BookCopyUpdateSchema(BaseModel):
    book_id: Optional[int] = None
    status: Optional[BookStatus] = None


class BookCopyPublicSchema(BaseModel):
    id: int
    book: BookRelationshipPublicSchema
    status: BookStatus
    created_at: datetime
    updated_at: datetime


class BookCopyCreateListPublicSchema(BaseModel):
    copies: List[BookCopyPublicSchema]
    quantity: int


class BookCopyListPublicSchema(BaseModel):
    book_copies: List[BookCopyPublicSchema]
    offset: int
    limit: int
