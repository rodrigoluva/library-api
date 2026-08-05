from fastapi import status


def test_create_author_success(client, admin_token, author_schema):
    response = client.post(
        'api/v1/authors',
        json=author_schema.model_dump(mode='json'),
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    response_data = response.json()
    author_data = author_schema.model_dump(mode='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['name'] == author_data['name']
    assert response_data['bio'] == author_data['bio']
    assert response_data['birthdate'] == author_data['birthdate']
    assert 'id' in response_data


def test_list_authors_success(client, user_token, author):
    response = client.get(
        'api/v1/authors',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'authors' in data
    assert data['offset'] == 0
    assert data['limit'] == 100


def test_list_authors_name_not_found(client, user_token):
    response = client.get(
        'api/v1/authors?search=namenotfound',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'name not found'


def test_get_author_success(client, user_token, author):
    response = client.get(
        f'api/v1/authors/{author.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK


def test_get_author_not_found(client, user_token):
    response = client.get(
        'api/v1/authors/9999',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'author not found'


def test_update_author_success(client, admin_token, author):
    response = client.put(
        f'api/v1/authors/{author.id}',
        json={'bio': 'updated bio'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data['bio'] == 'updated bio'
    assert data['name'] == author.name
    assert data['birthdate'] == author.birthdate.isoformat()


def test_update_author_not_found(client, admin_token):
    response = client.put(
        'api/v1/authors/999',
        json={'bio': 'updated bio'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'author not found'


def test_delete_author_success(client, admin_token, author):
    response = client.delete(
        f'api/v1/authors/{author.id}',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_author_not_found(client, admin_token):
    response = client.delete(
        'api/v1/authors/9999',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'author not found'
