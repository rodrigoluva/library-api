from fastapi import status


def test_borrow_book_success(
    client,
    user_token,
    book,
    book_copy,
):
    response = client.post(
        f'api/v1/books/{book.id}/borrow',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data['book_copy_id'] == book_copy.id
    assert data['returned_at'] is None
    assert data['borrowed_at'] is not None
    assert data['due_at'] is not None


def test_borrow_book_not_found(
    client,
    user_token,
):
    response = client.post(
        'api/v1/books/999/borrow',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book not found'


def test_borrow_book_already_borrowed(
    client,
    user_token,
    borrowed_record,
    book,
):
    response = client.post(
        f'api/v1/books/{book.id}/borrow',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == (
        'you already have a copy of this book borrowed'
    )


def test_borrow_book_copies_unavailable(
    client,
    user_2_token,
    book,
    book_copy,
    borrowed_record,
):
    response = client.post(
        f'api/v1/books/{book.id}/borrow',
        headers={'Authorization': f'Bearer {user_2_token}'},
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == (
        'no available copies'
    )


def test_return_book_success(
        client,
        user_token,
        book,
        borrowed_record,
):
    response = client.post(
        f'api/v1/books/{book.id}/return',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_200_OK


def test_return_book_not_found(
        client,
        user_token,
):
    response = client.post(
        'api/v1/books/999/return',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'book not found'


def test_return_book_no_active_borrow(
        client,
        user_token,
        book,
):
    response = client.post(
        f'api/v1/books/{book.id}/return',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'no active borrow record found'


def test_list_borrow_records_success(
        client,
        admin_token,
        borrowed_record,
):
    response = client.get(
        'api/v1/borrow-records',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['offset'] == 0
    assert data['limit'] == 100
    assert 'borrow_records' in data


def test_list_borrow_records_filter_user_id(
        client,
        admin_token,
        borrowed_record,
):
    response = client.get(
        f'api/v1/borrow-records?user_id={borrowed_record.user_id}',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['offset'] == 0
    assert data['limit'] == 100
    assert 'borrow_records' in data
    assert data['borrow_records'][0]['user_id'] == borrowed_record.user_id


def test_list_borrow_records_filter_book_copy_id(
        client,
        admin_token,
        borrowed_record,
):
    response = client.get(
        f'api/v1/borrow-records?book_copy_id={borrowed_record.book_copy_id}',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['offset'] == 0
    assert data['limit'] == 100
    assert 'borrow_records' in data
    assert data['borrow_records'][0]['book_copy_id'] == (
        borrowed_record.book_copy_id
    )


def test_borrow_record_success(
        client,
        admin_token,
        borrowed_record,
):
    response = client.get(
        f'api/v1/borrow-records/{borrowed_record.id}',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK


def test_borrow_record_not_found(
        client,
        admin_token,
):
    response = client.get(
        'api/v1/borrow-records/999',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'borrow record not found'


def test_delete_borrow_record_success(
        client,
        admin_token,
        borrowed_record,
):
    response = client.delete(
        f'api/v1/borrow-records/{borrowed_record.id}',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_borrow_record_not_found(
        client,
        admin_token,
):
    response = client.delete(
        'api/v1/borrow-records/999',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'borrow record not found'
