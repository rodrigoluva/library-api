from fastapi import status

from library_api.models.books import BookStatus


def test_create_book_copy_success(client, admin_token, book):
    payload = {
        'quantity': 3,
    }

    response = client.post(
        f'api/v1/books/{book.id}/copies',
        json=payload,
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data['quantity'] == 3
    assert len(data['copies']) == 3

    for copy in data['copies']:
        assert copy['book']['id'] == book.id
        assert copy['status'] == BookStatus.AVAILABLE


def test_create_book_not_found(
    client,
    admin_token,
):
    payload = {
        'quantity': 3,
    }

    response = client.post(
        'api/v1/books/999/copies',
        json=payload,
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book not found'


def test_list_book_copies_success(
    client,
    user_token,
    book_copies,
):
    response = client.get(
        'api/v1/book-copies',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['offset'] == 0
    assert data['limit'] == 100
    assert 'book_copies' in data


def test_list_book_copies_search_title(
    client,
    user_token,
    book,
    book_copies,
):
    response = client.get(
        f'api/v1/book-copies?search={book.title}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK


def test_list_book_copies_filter_book_id(
    client,
    user_token,
    book,
    book_copies,
):
    response = client.get(
        f'api/v1/book-copies?book_id={book.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK


def test_list_book_copies_not_found(
    client,
    user_token,
):
    response = client.get(
        'api/v1/book-copies',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book copy not found'


def test_get_book_copy_success(
    client,
    user_token,
    book_copy,
):
    response = client.get(
        f'api/v1/book-copies/{book_copy.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK


def test_get_book_copy_not_found(
    client,
    user_token,
):
    response = client.get(
        'api/v1/book-copies/999',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book copy not found'


def test_update_book_copy_success(
    client,
    admin_token,
    book_copy,
):
    response = client.put(
        f'api/v1/book-copies/{book_copy.id}',
        json={'status': BookStatus.BORROWED},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == book_copy.id
    assert data['status'] == BookStatus.BORROWED


def test_update_book_copy_not_found(
    client,
    admin_token,
):
    response = client.put(
        'api/v1/book-copies/999',
        json={'status': BookStatus.BORROWED},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book copy not found'


def test_update_book_copy_book_not_found(client, admin_token, book_copy):
    response = client.put(
        f'api/v1/book-copies/{book_copy.id}',
        json={'book_id': 999},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book not found'


def test_delete_book_copy_success(
    client,
    admin_token,
    book_copy,
):
    response = client.delete(
        f'api/v1/book-copies/{book_copy.id}',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_book_copy_not_found(
    client,
    admin_token,
):
    response = client.delete(
        'api/v1/book-copies/999',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book copy not found'
