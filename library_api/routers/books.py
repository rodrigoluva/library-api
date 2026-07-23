from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from library_api.core.database import get_session
from library_api.dependencies.permissions import UserRole, require_roles
from library_api.models import Author, Book, BookCopy, User
from library_api.models.books import BookStatus
from library_api.schemas.books import (
    BookListPublicSchema,
    BookPublicSchema,
    BookRelationshipListPublicSchema,
    BookSchema,
    BookUpdateSchema,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=BookPublicSchema,
    summary='Create Book - [ADMIN, LIBRARIAN]',
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'content': {
                'application/json': {
                    'example': {'detail': 'isbn already in use'}
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            'content': {
                'application/json': {
                    'example': {'detail': 'Not authenticated'}
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            'content': {
                'application/json': {
                    'example': {'detail': 'not enough permissions'}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            'content': {
                'application/json': {'example': {'detail': 'author not found'}}
            }
        },
    },
)
async def create_book(
    book: BookSchema,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LIBRARIAN,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    isbn_exists = await db.scalar(
        select(exists().where(Book.isbn == book.isbn))
    )
    if isbn_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='isbn already in use',
        )

    author = await db.get(Author, book.author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='author not found',
        )

    db_book = Book(
        title=book.title,
        isbn=book.isbn,
        published_date=book.published_date,
        author_id=book.author_id,
    )

    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)

    return db_book


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=BookListPublicSchema,
    summary='List Books - [ADMIN, LIBRARIAN, MEMBER]',
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'content': {
                'application/json': {
                    'example': {'detail': 'Not authenticated'}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            'content': {
                'application/json': {'example': {'detail': 'book not found'}}
            }
        },
    },
)
async def list_books(
    offset: int = Query(0, ge=0, description='Number of records to skip'),
    limit: int = Query(100, ge=1, le=100, description='Limit of records'),
    search: Optional[str] = Query(
        None,
        description='Search by ISBN or title',
    ),
    author_id: Optional[str] = Query(
        None,
        description='Filter by Author ID',
    ),
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LIBRARIAN,
            UserRole.MEMBER,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    query = (
        select(
            Book,
            func.count(BookCopy.id).label('available_copies'),
        )
        .outerjoin(
            BookCopy,
            and_(
                Book.id == BookCopy.book_id,
                BookCopy.status == BookStatus.AVAILABLE,
            ),
        )
        .options(selectinload(Book.author))
        .group_by(Book.id)
    )

    if search:
        search_filter = f'%{search}%'
        query = query.where(
            (Book.isbn.ilike(search_filter))
            | (Book.title.ilike(search_filter))
        )

    if author_id is not None:
        query = query.where(Book.author_id == author_id)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    rows = result.all()

    books = []

    for book, available_copies in rows:
        book.available_copies = available_copies
        books.append(book)

    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book not found',
        )

    return {
        'books': books,
        'offset': offset,
        'limit': limit,
    }


@router.get(
    path='/{book_id}',
    status_code=status.HTTP_200_OK,
    response_model=BookRelationshipListPublicSchema,
    summary='Search Book by ID - [ADMIN, LIBRARIAN, MEMBER]',
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'content': {
                'application/json': {
                    'example': {'detail': 'Not authenticated'}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            'content': {
                'application/json': {'example': {'detail': 'book not found'}}
            }
        },
    },
)
async def get_book(
    book_id: int,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LIBRARIAN,
            UserRole.MEMBER,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    query = (
        select(
            Book,
            func.count(BookCopy.id).label('available_copies'),
        )
        .outerjoin(
            BookCopy,
            and_(
                Book.id == BookCopy.book_id,
                BookCopy.status == BookStatus.AVAILABLE,
            ),
        )
        .options(selectinload(Book.author))
        .where(Book.id == book_id)
        .group_by(Book.id)
    )

    result = await db.execute(query)

    row = result.first()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book not found',
        )

    book, available_copies = row
    book.available_copies = available_copies

    return book


@router.put(
    path='/{book_id}',
    status_code=status.HTTP_200_OK,
    response_model=BookPublicSchema,
    summary='Update Book - [ADMIN, LIBRARIAN]',
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'content': {
                'application/json': {
                    'example': {'detail': 'isbn already in use'},
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            'content': {
                'application/json': {
                    'example': {'detail': 'Not authenticated'}
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            'content': {
                'application/json': {
                    'example': {'detail': 'not enough permissions'}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            'content': {
                'application/json': {
                    'schema': {
                        'oneOf': [
                            {
                                'type': 'object',
                                'properties': {
                                    'detail': {
                                        'type': 'string',
                                        'example': 'book not found',
                                    },
                                },
                            },
                            {
                                'type': 'object',
                                'properties': {
                                    'detail': {
                                        'type': 'string',
                                        'example': 'author not found',
                                    },
                                },
                            },
                        ]
                    },
                    'examples': {
                        'book_not_found': {
                            'summary': 'Book not found',
                            'value': {'detail': 'book not found'},
                        },
                        'author_not_found': {
                            'summary': 'Author not found',
                            'value': {'detail': 'author not found'},
                        },
                    },
                },
            },
        },
    },
)
async def update_book(
    book_id: int,
    book_update: BookUpdateSchema,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LIBRARIAN,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book not found',
        )

    isbn_exists = await db.scalar(
        select(
            exists().where(
                Book.isbn == book_update.isbn,
                Book.id != book_id,
            )
        )
    )
    if isbn_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='isbn already in use',
        )

    author = await db.get(Author, book_update.author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='author not found',
        )

    update_data = book_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    await db.commit()
    await db.refresh(book)

    return book


@router.delete(
    path='/{book_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete Book - [ADMIN]',
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'content': {
                'application/json': {
                    'example': {'detail': 'Not authenticated'}
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            'content': {
                'application/json': {
                    'example': {'detail': 'not enough permissions'}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            'content': {
                'application/json': {'example': {'detail': 'book not found'}}
            }
        },
    },
)
async def delete_book(
    book_id: int,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    book = await db.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book not found',
        )

    await db.delete(book)
    await db.commit()
