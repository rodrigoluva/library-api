# Testing

The Library API uses **pytest** to ensure the correctness of the application through automated tests. The test suite covers authentication, authorization, endpoint behavior, request validation, and database interactions.

## Testing Stack

The project uses the following tools:

* **pytest** – Test runner.
* **pytest-asyncio** – Support for asynchronous tests.
* **FastAPI TestClient** – HTTP client for endpoint testing.
* **SQLite In-Memory Database** – Isolated database created for every test session.
* **SQLAlchemy Async** – Asynchronous database operations.

## Running the Tests

Run the complete test suite:

```bash
poetry run task test
```

## Test Database

Tests use an **SQLite in-memory database**, which provides:

* Fast execution.
* Isolation between test runs.
* No modification of the development database.
* Automatic database creation and cleanup.

Each test starts with a fresh database, ensuring that tests remain independent and reproducible.

## Test Structure

```
tests/
├── conftest.py
├── test_auth.py
├── test_authors.py
├── test_book_copies.py
├── test_books.py
├── test_borrow_records.py
├── test_db.py
├── test_health_check.py
└── test_users.py
```

### `conftest.py`

Shared fixtures are defined in `conftest.py`, including:

* Database session
* Test client
* Authentication tokens
* Sample users
* Authors
* Books
* Book copies
* Borrow records

Using fixtures reduces duplicated code and keeps tests concise.

## Testing Strategy

Each endpoint is tested for its primary behaviors, including:

* Successful requests
* Authentication (`401 Unauthorized`)
* Authorization (`403 Forbidden`)
* Resource not found (`404 Not Found`)
* Validation errors (`422 Unprocessable Entity`)
* Business rule violations (`400 Bad Request` / `409 Conflict`)

Whenever applicable, tests also verify that the database state changes correctly after an operation.

## Example Test

```python
def test_get_user_success(client, admin_token, user):
    response = client.get(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user.id
    assert data["email"] == user.email
```

## Fixtures

Fixtures provide reusable test data and dependencies.

Examples include:

* `client`
* `session`
* `admin_token`
* `librarian_token`
* `member_token`
* `user`
* `author`
* `book`
* `book_copy`
* `borrowed_record`

Using fixtures keeps tests focused on their expected behavior instead of setup logic.

## Best Practices

* Keep tests independent.
* Create only the data required for each test.
* Prefer fixtures over duplicated setup code.
* Verify both the HTTP response and database changes.
* Write descriptive test names that clearly express the expected behavior.
* Test success paths as well as failure scenarios.

## Continuous Testing

Before opening a pull request or merging changes, run the complete test suite to ensure that new changes do not introduce regressions.

A passing test suite helps maintain the reliability and stability of the Library API as the project evolves.
