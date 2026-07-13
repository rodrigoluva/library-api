from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from library_api.core.database import get_session
from library_api.models import Author
from library_api.schemas.authors import (
    AuthorListPublicSchema,
    AuthorPublicSchema,
    AuthorSchema,
    AuthorUpdateSchema,
)


router = APIRouter()

@router.post(
        path='/',
        status_code=status.HTTP_201_CREATED,
        response_model=AuthorPublicSchema,
        summary='Create Author',
)
async def create_author(
        author: AuthorSchema,
        db: AsyncSession = Depends(get_session),
):
    db_author = Author(
        name=author.name,
        bio=author.bio,
        birthdate=author.birthdate,
    )

    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)

    return db_author


@router.get(
        path='/',
        status_code=status.HTTP_200_OK,
        response_model=AuthorListPublicSchema,
        summary='List Authors',
        responses={
            status.HTTP_404_NOT_FOUND: {
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'user not found'
                        }
                    }
                }
            },
        },
)
async def list_authors(
        offset: int = Query(0, ge=0, description='Number of records to skip'),
        limit: int = Query(100, ge=1, le=100, description='Limit of records'),
        search: Optional[str] = Query(None, description='Search by name'),
        db: AsyncSession = Depends(get_session),
):
    query = select(Author)

    if search:
        search_filter = f'%{search}%'
        query = query.where(
            Author.name.ilike(search_filter)
        )
    
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    authors = result.scalars().all()

    if not authors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='name not found',
        )
    
    return {
        'authors': authors,
        'offset': offset,
        'limit': limit,
    }

@router.get(
        path='/{author_id}',
        status_code=status.HTTP_200_OK,
        response_model=AuthorPublicSchema,
        summary='Search Author by ID',
        responses={
            status.HTTP_404_NOT_FOUND: {
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'user not found'
                        }
                    }
                }
            },
        },
)
async def get_author(
        author_id: int,
        db: AsyncSession = Depends(get_session),
):
    author = await db.get(Author, author_id)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found',
        )
    
    return author


@router.put(
        path='/{author_id}',
        status_code=status.HTTP_200_OK,
        response_model=AuthorPublicSchema,
        summary='Update Author',
        responses={
            status.HTTP_404_NOT_FOUND: {
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'user not found'
                        }
                    }
                }
            },
        },

)
async def update_author(
        author_id: int,
        author_update: AuthorUpdateSchema,
        db: AsyncSession = Depends(get_session), 
):
    author = await db.get(Author, author_id)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found',
        )
    
    update_data = author_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(author, field, value)
    
    await db.commit()
    await db.refresh(author)

    return author


@router.delete(
        path='/{author_id}',
        status_code=status.HTTP_204_NO_CONTENT,
        summary='Delete Author',
        responses={
            status.HTTP_404_NOT_FOUND: {
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'user not found'
                        }
                    }
                }
            },
        },
)
async def delete_author(
        author_id: int,
        db: AsyncSession = Depends(get_session),
):
    author = await db.get(Author, author_id)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='author not found',
        )

    await db.delete(author)
    await db.commit()

    return
