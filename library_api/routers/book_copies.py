from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from library_api.core.database import get_session
from library_api.dependencies.permissions import User, UserRole, require_roles
from library_api.models.books import Book, BookCopy, BookStatus
from library_api.schemas.book_copies import (
    BookCopyCreateListPublicSchema,
    BookCopyCreateSchema,
    BookCopyListPublicSchema,
    BookCopyPublicSchema,
    BookCopyUpdateSchema,
)

router = APIRouter()


@router.post(
    path='/books/{book_id}/copies',
    status_code=status.HTTP_200_OK,
    response_model=BookCopyCreateListPublicSchema,
    summary='Create copies of a Book - [ADMIN, LIBRARIAN]',
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
async def create_book_copy(
    book_id: int,
    data: BookCopyCreateSchema,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LIBRARIAN,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    book_result = await db.execute(select(Book).where(Book.id == book_id))
    book = book_result.scalar_one_or_none()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book not found',
        )

    copies = [
        BookCopy(
            book_id=book_id,
            status=BookStatus.AVAILABLE,
        )
        for _ in range(data.quantity)
    ]

    db.add_all(copies)
    await db.commit()

    book_copies_result = await db.execute(
        select(BookCopy)
        .options(selectinload(BookCopy.book).selectinload(Book.author))
        .where(BookCopy.book_id == book_id)
        .order_by(BookCopy.id.desc())
        .limit(data.quantity)
    )
    created_copies = list(reversed(book_copies_result.scalars().all()))

    return {'copies': created_copies, 'quantity': data.quantity}


@router.get(
    path='/book-copies',
    status_code=status.HTTP_200_OK,
    response_model=BookCopyListPublicSchema,
    summary='List Book Copies - [ADMIN, LIBRARIAN]',
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
                'application/json': {
                    'example': {'detail': 'book copy not found'}
                }
            }
        },
    },
)
async def list_book_copies(
    offset: int = Query(0, ge=0, description='Number of records to skip'),
    limit: int = Query(100, ge=1, le=100, description='Limit of records'),
    search: Optional[str] = Query(None, description='Search by Book name'),
    book_id: Optional[int] = Query(None, description='Filter by Book ID'),
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
        select(BookCopy)
        .join(BookCopy.book)
        .options(selectinload(BookCopy.book).selectinload(Book.author))
    )

    if search:
        search_filter = f'%{search}%'
        query = query.where(Book.title.ilike(search_filter))

    if book_id is not None:
        query = query.where(BookCopy.book_id == book_id)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    book_copies = result.scalars().all()

    if not book_copies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book copy not found',
        )

    return {
        'book_copies': book_copies,
        'offset': offset,
        'limit': limit,
    }


@router.get(
    path='/book-copies/{book_copy_id}',
    status_code=status.HTTP_200_OK,
    response_model=BookCopyPublicSchema,
    summary='Search Book Copy by ID - [ADMIN, LIBRARIAN]',
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
                'application/json': {
                    'example': {'detail': 'book copy not found'}
                }
            }
        },
    },
)
async def get_book_copy(
    book_copy_id: int,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LIBRARIAN,
            UserRole.MEMBER,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(
        select(BookCopy)
        .options(selectinload(BookCopy.book).selectinload(Book.author))
        .where(BookCopy.id == book_copy_id)
    )

    book_copy = result.scalar_one_or_none()
    if not book_copy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book copy not found',
        )

    return book_copy


@router.put(
    path='/book-copies/{book_copy_id}',
    status_code=status.HTTP_200_OK,
    response_model=BookCopyPublicSchema,
    summary='Update Book Copy - [ADMIN, LIBRARIAN]',
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
                'application/json': {
                    'schema': {
                        'oneOf': [
                            {
                                'type': 'object',
                                'properties': {
                                    'detail': {
                                        'type': 'string',
                                        'example': 'book copy not found',
                                    },
                                },
                            },
                            {
                                'type': 'object',
                                'properties': {
                                    'detail': {
                                        'type': 'string',
                                        'example': 'book not found',
                                    },
                                },
                            },
                        ]
                    },
                    'examples': {
                        'book_copy_found': {
                            'summary': 'Book Copy not found',
                            'value': {'detail': 'book copy not found'},
                        },
                        'book_not_found': {
                            'summary': 'Book not found',
                            'value': {'detail': 'book not found'},
                        },
                    },
                },
            },
        },
    },
)
async def update_book_copy(
    book_copy_id: int,
    book_copy_update: BookCopyUpdateSchema,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LIBRARIAN,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    book_copy = await db.get(BookCopy, book_copy_id)
    if not book_copy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book copy not found',
        )

    update_data = book_copy_update.model_dump(exclude_unset=True)

    if 'book_id' in update_data:
        book_exists = await db.scalar(
            select(exists().where(Book.id == update_data['book_id']))
        )
        if not book_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='book not found',
            )

    for field, value in update_data.items():
        setattr(book_copy, field, value)

    await db.commit()
    await db.refresh(book_copy)

    result = await db.execute(
        select(BookCopy)
        .options(selectinload(BookCopy.book).selectinload(Book.author))
        .where(BookCopy.id == book_copy_id)
    )
    book_copy_with_relations = result.scalar_one()

    return book_copy_with_relations


@router.delete(
    path='/book-copies/{book_copy_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete Book Copy - [ADMIN]',
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
                'application/json': {
                    'example': {'detail': 'book copy not found'}
                }
            }
        },
    },
)
async def delete_book_copy(
    book_copy_id: int,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    book_copy = await db.get(BookCopy, book_copy_id)

    if not book_copy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book copy not found',
        )

    await db.delete(book_copy)
    await db.commit()
