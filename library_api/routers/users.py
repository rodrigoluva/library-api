from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from library_api.core.database import get_session
from library_api.core.security import get_password_hash
from library_api.models import User
from library_api.schemas.users import (
    UserListPublicSchema,
    UserPublicSchema,
    UserSchema,
    UserUpdateSchema,
)


router = APIRouter()


@router.post(
        path='/',
        status_code=status.HTTP_201_CREATED,
        response_model=UserPublicSchema,
        summary='Create User',
        responses={
            status.HTTP_400_BAD_REQUEST: {
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'email not available'
                        }
                    }
                }
            },
        },
)
async def create_user(
        user: UserSchema,
        db: AsyncSession = Depends(get_session),
):
    email_exists = await db.scalar(
        select(exists().where(User.email == user.email))
    )
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='email not available'
        )

    db_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        name=user.name,
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


@router.get(
        path='/',
        status_code=status.HTTP_200_OK,
        response_model=UserListPublicSchema,
        summary='List Users',
        responses={
            status.HTTP_404_NOT_FOUND: {
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'user or email not found'
                        }
                    }
                }
            },
        },
)
async def list_users(
        offset: int = Query(0, ge=0, description='number of records to skip'),
        limit: int = Query(100, ge=1, le=100, description='limit of records'),
        search: Optional[str] = Query(None, description='Search by name or email'),
        db: AsyncSession = Depends(get_session),
):
    query = select(User)

    if search:
        search_filter = f'%{search}%'
        query = query.where(
            (User.name.ilike(search_filter))
            | (User.email.ilike(search_filter))
        )

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    users = result.scalars().all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='name or email not found'
        )

    return {
        'users': users,
        'offset': offset,
        'limit': limit,
    }


@router.get(
        path='/{user_id}',
        status_code=status.HTTP_200_OK,
        response_model=UserPublicSchema,
        summary='Search User by ID',
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
async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_session),
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found',
        )

    return user


@router.put(
        path='/{user_id}',
        status_code=status.HTTP_201_CREATED,
        response_model=UserPublicSchema,
        summary='Update User',
        responses={
            status.HTTP_400_BAD_REQUEST: {
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'email not available'
                        }
                    }
                }
            },
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
async def update_user(
        user_id: int,
        user_update: UserUpdateSchema,
        db: AsyncSession = Depends(get_session)
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    
    update_data = user_update.model_dump(exclude_unset=True)

    if 'email' in update_data and update_data['email'] != user.email:
        email_exists = await db.scalar(
            select(exists().where(
                (User.email == update_data['email']) &
                (User.id != user_id)
            ))
        )
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='email not available',
            )

    if 'password' in update_data:
        update_data['password'] = get_password_hash(update_data['password'])
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)

    return user


@router.delete(
        path='/{user_id}',
        status_code=status.HTTP_204_NO_CONTENT,
        summary='Delete User',
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
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_session),
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found',
        )

    await db.delete(user)
    await db.commit()

    return
