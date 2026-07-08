from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from library_api.models import Base


class BookStatus(str, Enum):
    AVAILABLE = 'available'
    BORROWED = 'borrowed'


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    bio: Mapped[Optional[str]] = mapped_column(Text, default=None)
    birthdate: Mapped[Optional[date]]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        server_default=func.now(),
    )

    books: Mapped[List['Book']] = relationship(
        'Book',
        back_populates='authors'
    )


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    isbn: Mapped[str] = mapped_column(unique=True, index=True)
    published_date: Mapped[Optional[date]]
    author_id: Mapped[int] = mapped_column(
        ForeignKey('authors.id'),
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        server_default=func.now(),
    )

    author: Mapped['Author'] = relationship(
        'Author',
        back_populates='books'
    )

    book_copies: Mapped[List['BookCopy']] = relationship(
        'BookCopy',
        back_populates='books'
    )


class BookCopy(Base):
    __tablename__ = 'book_copies'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id')
    )
    status: Mapped[BookStatus] = mapped_column(String(15))
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        server_default=func.now(),
    )

    book: Mapped['Book'] = relationship(
        'Book',
        back_populates='book_copies'
    )
