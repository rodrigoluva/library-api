import pytest
from fastapi import status

from library_api.core.security import verify_password
from library_api.models import User


def test_create_member_user_success(client, user_data_schema):
    response = client.post(
        'api/v1/users/',
        json=user_data_schema.model_dump(),
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data['email'] == user_data_schema.email
    assert data['name'] == user_data_schema.name
    assert data['role'] == 'member'

    assert 'password' not in data


def test_create_user_email_unavailable(client, user, user_data_schema):
    response = client.post(
        'api/v1/users/',
        json=user_data_schema.model_dump(),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_users_success(client, admin_token):
    response = client.get(
        'api/v1/users',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'users' in data
    assert data['offset'] == 0
    assert data['limit'] == 100


def test_list_users_search_by_name(client, admin_token):
    response = client.get(
        'api/v1/users?search=admin',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    users = response.json()['users']

    assert users[0]['name'] == 'Admin'


def test_list_users_not_found(client, admin_token):
    response = client.get(
        'api/v1/users?search=doesnotexist',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'name or email not found',
    }


def test_get_user_success(client, admin_token, user):
    response = client.get(
        f'api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['id'] == user.id
    assert data['name'] == user.name
    assert data['email'] == user.email


def test_get_user_not_found(client, admin_token):
    response = client.get(
        'api/v1/users/9999',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'user not found',
    }


def test_update_user_success(client, admin_token, user):
    payload = {
        'name': 'Updated Name',
        'email': 'updated@example.com',
    }

    response = client.put(
        f'api/v1/users/{user.id}',
        json=payload,
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['name'] == payload['name']
    assert data['email'] == payload['email']


def test_update_user_not_found(client, admin_token):
    payload = {
        'name': 'Updated Name',
        'email': 'updated@example.com',
    }

    response = client.put(
        'api/v1/users/999',
        json=payload,
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'user not found'


def test_update_user_email_unavailable(client, admin_token, user, admin_user):
    payload = {'email': f'{admin_user.email}'}

    response = client.put(
        f'api/v1/users/{user.id}',
        json=payload,
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'email not available'


@pytest.mark.asyncio
async def test_update_user_email(client, session, admin_token, user):
    new_password = 'newpassword123'

    response = client.put(
        f'api/v1/users/{user.id}',
        json={'password': new_password},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    updated_user = await session.get(User, user.id)

    assert verify_password(new_password, updated_user.password)


def test_delete_user_success(client, admin_token, user):
    response = client.delete(
        f'api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user_not_found(client, admin_token):
    response = client.delete(
        'api/v1/users/9999',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'user not found'


def test_delete_user_forbidden(client, user_token, user):
    response = client.delete(
        f'api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'not enough permissions'
