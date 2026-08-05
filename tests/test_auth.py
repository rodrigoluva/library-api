from datetime import UTC, datetime, timedelta

import jwt
import pytest
from fastapi import HTTPException, status

from library_api.core.security import create_access_token, verify_token
from library_api.core.settings import Settings

settings = Settings()


def test_token_success(client, user_data, user):
    login_data = {
        'email': user_data['email'],
        'password': user_data['password'],
    }

    response = client.post('/api/v1/token', json=login_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
    assert isinstance(data['access_token'], str)
    assert len(data['access_token']) > 0


def test_token_unauthorized(client, user_data):
    login_data = {
        'email': user_data['email'],
        'password': user_data['password'],
    }

    response = client.post('/api/v1/token', json=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert 'detail' in data
    assert data['detail'] == 'incorrect email or password'


def test_verify_token_sucess():
    token = create_access_token({'sub': '1'})

    payload = verify_token(token)

    assert payload['sub'] == '1'


def test_verify_token_expired():
    token = jwt.encode(
        {
            'sub': '1',
            'exp': datetime.now(UTC) - timedelta(minutes=1),
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc:
        verify_token(token)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == 'token has expired'


def test_verify_token_invalid():
    with pytest.raises(HTTPException) as exc:
        verify_token('not-a-token')

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == 'could not validate credentials'


def test_refresh_token_success(client, user_token):
    response = client.post(
        'api/v1/refresh_token',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
