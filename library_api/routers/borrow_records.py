from datetime import UTC, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from library_api.core.database import get_session
from library_api.dependencies.permissions import (
    User,
    UserRole,
    get_current_user,
    require_roles,
)
from library_api.models import Book, BookCopy, BorrowRecord
from library_api.models.books import BookStatus
from library_api.schemas.borrow_records import (
    BorrowRecordListSchema,
    BorrowRecordPublicSchema,
)

router = APIRouter()


@router.post(
    path='/books/{book_id}/borrow',
    status_code=status.HTTP_201_CREATED,
    response_model=BorrowRecordPublicSchema,
    summary='Borrow Book - [ADMIN, LIBRARIAN, MEMBER]',
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
        status.HTTP_409_CONFLICT: {
            'content': {
                'application/json': {
                    'schema': {
                        'oneOf': [
                            {
                                'type': 'object',
                                'properties': {
                                    'detail': {
                                        'type': 'string',
                                        'example': 'you already have a copy of this book borrowed',  # noqa: E501
                                    },
                                },
                            },
                            {
                                'type': 'object',
                                'properties': {
                                    'detail': {
                                        'type': 'string',
                                        'example': 'no available copies',
                                    },
                                },
                            },
                        ]
                    },
                    'examples': {
                        'book_copy_borrowed': {
                            'summary': 'Have a copy',
                            'value': {
                                'detail': 'you already have a copy of this book borrowed'  # noqa: E501
                            },
                        },
                        'book_copy_not_available': {
                            'summary': 'No available copies',
                            'value': {'detail': 'no available copies'},
                        },
                    },
                },
            },
        },
    },
)
async def borrow_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    book = await db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book not found',
        )

    existing_borrow = await db.scalar(
        select(BorrowRecord)
        .join(BookCopy)
        .where(
            BorrowRecord.user_id == current_user.id,
            BorrowRecord.returned_at.is_(None),
            BookCopy.book_id == book_id,
        )
    )

    if existing_borrow:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='you already have a copy of this book borrowed',
        )

    book_copy = await db.scalar(
        select(BookCopy)
        .where(
            BookCopy.book_id == book_id,
            BookCopy.status == BookStatus.AVAILABLE,
        )
        .limit(1)
    )

    if book_copy is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='no available copies',
        )

    borrow_record = BorrowRecord(
        user_id=current_user.id,
        book_copy_id=book_copy.id,
        borrowed_at=datetime.now(UTC),
        due_at=datetime.now(UTC) + timedelta(days=14),
    )

    book_copy.status = BookStatus.BORROWED

    db.add(borrow_record)
    await db.commit()
    await db.refresh(borrow_record)

    return borrow_record


@router.post(
    path='/books/{book_id}/return',
    status_code=status.HTTP_200_OK,
    response_model=BorrowRecordPublicSchema,
    summary='Return Book - [ADMIN, LIBRARIAN, MEMBER]',
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
        status.HTTP_409_CONFLICT: {
            'content': {
                'application/json': {
                    'example': {'detail': 'no available copies'}
                }
            }
        },
    },
)
async def return_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    book = await db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='book not found',
        )

    result = await db.execute(
        select(BorrowRecord)
        .options(selectinload(BorrowRecord.book_copy))
        .join(BookCopy)
        .where(
            BorrowRecord.user_id == current_user.id,
            BorrowRecord.returned_at.is_(None),
            BookCopy.book_id == book_id,
        )
    )
    borrow_record = result.scalar_one_or_none()

    if borrow_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='no active borrow record found',
        )

    borrow_record.returned_at = datetime.now(UTC)
    borrow_record.book_copy.status = BookStatus.AVAILABLE

    await db.commit()
    await db.refresh(borrow_record)

    return borrow_record


@router.get(
    path='/borrow-records',
    status_code=status.HTTP_200_OK,
    response_model=BorrowRecordListSchema,
    summary='List Borrow Records - [ADMIN, LIBRARIAN]',
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
    },
)
async def list_borrow_records(
    offset: int = Query(0, ge=0, description='Number of records to skip'),
    limit: int = Query(100, ge=1, le=100, description='Limit of records'),
    user_id: Optional[int] = Query(
        None,
        ge=1,
        description='Filter by User ID',
    ),
    book_copy_id: Optional[int] = Query(
        None,
        ge=1,
        description='Filter by Book Copy ID',
    ),
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LIBRARIAN,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    query = select(BorrowRecord)

    if user_id is not None:
        query = query.where(BorrowRecord.user_id == user_id)

    if book_copy_id is not None:
        query = query.where(BorrowRecord.book_copy_id == book_copy_id)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    borrow_records = result.scalars().all()

    return {
        'borrow_records': borrow_records,
        'offset': offset,
        'limit': limit,
    }


@router.get(
    path='/borrow-records/{borrow_record_id}',
    status_code=status.HTTP_200_OK,
    response_model=BorrowRecordPublicSchema,
    summary='Search Borrow Record by ID - [ADMIN, LIBRARIAN]',
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
                    'example': {'detail': 'borrow record not found'}
                }
            }
        },
    },
)
async def get_borrow_record(
    borrow_record_id: int,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LIBRARIAN,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    borrow_record = await db.get(BorrowRecord, borrow_record_id)

    if borrow_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='borrow record not found',
        )

    return borrow_record


@router.delete(
    path='/borrow-records/{borrow_record_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete Borrow Record - [ADMIN]',
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
                    'example': {'detail': 'borrow record not found'}
                }
            }
        },
    },
)
async def delete_borrow_record(
    borrow_record_id: int,
    _: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
    db: AsyncSession = Depends(get_session),
):
    borrow_record = await db.get(BorrowRecord, borrow_record_id)
    if not borrow_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='borrow record not found',
        )

    await db.delete(borrow_record)
    await db.commit()
