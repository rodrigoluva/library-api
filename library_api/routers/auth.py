from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from library_api.core.database import get_session
from library_api.core.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from library_api.models import User
from library_api.schemas.auth import LoginRequest, Token


router = APIRouter()


@router.post(
        path='/token',
        status_code=status.HTTP_200_OK,
        response_model=Token,
        summary='Create Access Token - [PUBLIC]',
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'incorrect email or password',
                        }
                    }
                }
            },
        },
)
async def token(
        login_data: LoginRequest,
        db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(
        email=login_data.email,
        password=login_data.password,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    access_token = create_access_token(
        data={'sub': str(user.id)}
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }


@router.post(
        path='/refresh_token',
        status_code=status.HTTP_200_OK,
        response_model=Token,
        summary='Refresh Access Token - [ADMIN, LIBRARIAN, MEMBER]',
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'could not validate credentials',
                        }
                    }
                }
            },
        },
)
async def refresh_token(
        current_user: User = Depends(get_current_user),
):
    access_token = create_access_token(
        data={'sub': str(current_user.id)}
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }