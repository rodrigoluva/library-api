from fastapi import status


def test_create_book_success(client, admin_token, book_schema):
    response = client.post(
        'api/v1/books',
        json=book_schema.model_dump(mode='json'),
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    book_data = book_schema.model_dump()

    assert response_data['title'] == book_data['title']
    assert response_data['isbn'] == book_data['isbn']
    assert (
        response_data['published_date']
        == book_data['published_date'].isoformat()
    )
    assert response_data['author_id'] == book_data['author_id']
    assert 'id' in response_data


def test_create_book_isbn_already_exists(
    client,
    admin_token,
    book_schema,
    book,
):
    book_schema.isbn = book.isbn

    response = client.post(
        'api/v1/books',
        json=book_schema.model_dump(mode='json'),
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'isbn already in use'


def test_create_book_author_not_found(
    client,
    admin_token,
    book_schema,
):
    book_schema.author_id = 999

    response = client.post(
        'api/v1/books',
        json=book_schema.model_dump(mode='json'),
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'author not found'


def test_list_books_success(
    client,
    user_token,
    book,
):
    response = client.get(
        'api/v1/books',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'books' in data
    assert data['offset'] == 0
    assert data['limit'] == 100


def test_list_books_search_isbn(
    client,
    user_token,
    book,
):
    response = client.get(
        f'api/v1/books?search={book.isbn}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK


def test_list_books_filter_author_id(
    client,
    user_token,
    book,
):
    response = client.get(
        f'api/v1/books?author_id={book.author_id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK


def test_list_books_not_found(
    client,
    user_token,
):
    response = client.get(
        'api/v1/books',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book not found'


def test_get_book_success(
    client,
    user_token,
    book,
):
    response = client.get(
        f'api/v1/books/{book.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK


def test_get_book_not_found(
    client,
    user_token,
):
    response = client.get(
        'api/v1/books/999',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book not found'


def test_update_book_success(
    client,
    admin_token,
    book,
):
    response = client.put(
        f'api/v1/books/{book.id}',
        json={'title': '1984 Test'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == '1984 Test'


def test_update_book_not_found(
    client,
    admin_token,
):
    response = client.put(
        'api/v1/books/999',
        json={'title': '1984 Test'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book not found'


def test_update_book_isbn_exists(
    client,
    admin_token,
    book,
    book_2,
):
    response = client.put(
        f'api/v1/books/{book.id}',
        json={'isbn': book_2.isbn},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'isbn already in use'


def test_update_book_author_not_found(
    client,
    admin_token,
    book,
):
    response = client.put(
        f'api/v1/books/{book.id}',
        json={'author_id': 999},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'author not found'


def test_delete_book_success(
    client,
    admin_token,
    book,
):
    response = client.delete(
        f'api/v1/books/{book.id}',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_book_not_found(
    client,
    admin_token,
):
    response = client.delete(
        'api/v1/books/999',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book not found'
