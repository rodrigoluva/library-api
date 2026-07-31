# Guidelines & Standards

Code style, architecture patterns, and best practices for the Library API project.

---

## Python Code Style

### Formatting & Linting (Ruff)

```bash
# Check style
poetry run task lint

# Auto-fix
poetry run task pre_format

# Format only
poetry run task format
```

**Ruff Configuration** (`pyproject.toml`):
```toml
[tool.ruff]
line-length = 79
preview = true

[tool.ruff.lint]
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
ignore = ['PLR2004', 'PLR0917', 'PLR0913']

[tool.ruff.format]
preview = true
quote-style = 'single'
```

### Key Style Rules

- **Line length:** Maximum of 79 characters.
- **Quotes:** Use single quotes (`'`).
- **Imports:** Keep imports sorted using isort (Ruff rule `I`).
- **Type hints:** Required for all public functions.
- **Async:** Use `async def` for all I/O functions.

---

## Architecture Patterns

### Layer Structure

```
library_api/
├── app.py                 # FastAPI app factory
├── cli.py                 # Typer CLI commands
├── core/                  # Cross-cutting concerns
│   ├── database.py        # Async engine & session
│   ├── security.py        # Auth, JWT, password hashing
│   └── settings.py        # Pydantic Settings
├── dependencies/          # FastAPI dependencies
│   └── permissions.py     # Role-based access control
├── models/                # SQLAlchemy ORM models
│   ├── base.py            # DeclarativeBase
│   ├── users.py           # User model + Role enum
│   └── books.py           # Author, Book, BookCopy, BorrowRecord
├── routers/               # API endpoints (controllers)
│   ├── auth.py            # /token, /refresh_token
│   ├── users.py           # /users/*
│   ├── authors.py         # /authors/*
│   ├── books.py           # /books/*
│   ├── book_copies.py     # /book-copies/*, /books/{id}/copies
│   └── borrow_records.py  # /borrow-records/*, /books/{id}/borrow|return
└── schemas/               # Pydantic v2 models (API contracts)
    ├── auth.py
    ├── users.py
    ├── authors.py
    ├── books.py
    ├── book_copies.py
    └── borrow_records.py
```

---

## Naming Conventions


- **Packages/Modules:** use `snake_case`.
    - Example: `book_copies.py`.
- **Classes:** use `PascalCase`.
    - Examples: `BookCopy`, `UserRole`.
- **Functions/Methods:** use `snake_case`.
    - Example: `create_book_copy()`.
- **Variables:** use `snake_case`.
    - Example: `book_copy_id`.
- **Constants:** use `UPPER_SNAKE_CASE`.
    - Example: `JWT_EXPIRATION_MINUTES`.
- **Enums:** use `PascalCase` for enum classes and access members as `EnumClass.MEMBER`.
    - Example: `UserRole.ADMIN`.
- **Database Tables:** use plural `snake_case`.
    - Example: `book_copies`.
- **Database Columns:** use `snake_case`.
    - Example: `created_at`.
- **API Paths:** use plural `kebab-case`.
    - Example: `/book-copies`.
- **Query Params:** use `snake_case`.
    - Example: `book_copy_id`.
- **Schema Classes:** use `PascalCase` with descriptive suffix.
    - Examples: `BookCopyCreateSchema`, `BookCopyPublicSchema`.

### Schema Naming Pattern

```
{Entity}{Operation}Schema
│
├── CreateSchema     # POST request body
├── UpdateSchema     # PUT/PATCH request body (all optional)
├── PublicSchema     # Single object response
├── ListPublicSchema # Paginated list response
└── Relationship...  # Nested relationships
```

---

## Security Guidelines

### Authentication

- **Never log passwords or tokens**
- **Use `pwdlib` with Argon2** for password hashing (already configured)
- **JWT tokens**: Short expiration (5-15 min), secure secret
- **HTTPS only** in production
- **Validate all inputs** with Pydantic schemas

### Authorization

- **Role-based access** via `require_roles()` dependency
- **Explicit permissions** per endpoint
- **Admin-only** for destructive operations (DELETE)
- **Member access** limited to own data (borrow/return own books)

### Data Protection

- **Never expose password hashes** in responses
- **Use separate schemas** for input vs output
- **Sanitize error messages** (no stack traces in production)
- **Rate limiting** (recommended for production)

---

## Database Guidelines

### Migrations (Alembic)

```bash
# Create migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback
poetry run alembic downgrade -1
```

### Migration Naming

```
{revision}_{description}.py
# Examples:
b9e0f87139b3_create_users_table.py
d58754e7c566_create_authors_books_book_copies_and_borrow_records.py
2f8a67030948_feat_add_users_role.py
```

### Model Guidelines

- **Inherit from `Base`** (`library_api.models.base.Base`)
- **Use `Mapped` + `mapped_column`** (SQLAlchemy 2.0 style)
- **Define relationships** with `relationship()` and `back_populates`
- **Use `TYPE_CHECKING`** for forward references
- **Add `created_at` / `updated_at`** to all tables
- **Use enums** for fixed-value columns (`UserRole`, `BookStatus`)

---

## API Design Guidelines

### REST Conventions

| Operation | Method | Path | Status | Body |
|-----------|--------|------|--------|------|
| List | GET | `/resource` | 200 | - |
| Create | POST | `/resource` | 201 | CreateSchema |
| Get One | GET | `/resource/{id}` | 200 | - |
| Update | PUT | `/resource/{id}` | 200 | UpdateSchema |
| Delete | DELETE | `/resource/{id}` | 204 | - |
| Custom Action | POST | `/resource/{id}/action` | 200/201 | Schema |

### Response Patterns

```python
# Single object
return db_object  # Auto-serialized via response_model

# Paginated list
return {
    "items": objects,
    "offset": offset,
    "limit": limit,
}

# Custom action response
return {"copies": created_copies, "quantity": quantity}
```

### Error Responses

| Status | When | Format |
|--------|------|--------|
| 400 | Business rule violation | `{"detail": "isbn already in use"}` |
| 401 | Missing/invalid token | `{"detail": "Not authenticated"}` |
| 403 | Insufficient permissions | `{"detail": "not enough permissions"}` |
| 404 | Resource not found | `{"detail": "book not found"}` |
| 409 | Conflict (e.g., already borrowed) | `{"detail": "no available copies"}` |
| 422 | Validation error | Pydantic error format |

---

## Testing Guidelines

### Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Pytest fixtures
├── test_auth.py         # Authentication tests
├── test_users.py        # User CRUD tests
├── test_authors.py      # Author CRUD tests
├── test_books.py        # Book CRUD tests
├── test_book_copies.py  # Copy CRUD tests
└── test_borrow_records.py # Borrow flow tests
```

### Test Patterns

```python
# Use async fixtures
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Test public endpoints
async def test_create_user(async_client):
    response = await async_client.post("/api/v1/users/", json={...})
    assert response.status_code == 201

# Test protected endpoints
async def test_list_users_admin(async_client, admin_token):
    response = await async_client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
```

---

## Dependency Management

### Adding Dependencies

```bash
# Production dependency
poetry add package-name

# Development dependency
poetry add --group dev package-name

# Optional dependency group
poetry add --group optional package-name
```

### Version Pinning

```toml
# pyproject.toml
dependencies = [
    "fastapi[standard] (>=0.139.0,<0.140.0)",  # Upper bound prevents breaking changes
]
```

---

## Documentation Standards

### OpenAPI Annotations

```python
@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=BookPublicSchema,
    summary='Create Book - [ADMIN, LIBRARIAN]',
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'content': {
                'application/json': {
                    'example': {'detail': 'isbn already in use'}
                }
            }
        },
    },
)
```

---

## Git Workflow

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feat/{short-description}` | `feat/add-borrow-records-crud` |
| Fix | `fix/{short-description}` | `fix/token-refresh-expiry` |
| Docs | `docs/{short-description}` | `docs/add-mkdocs` |
| Chore | `chore/{short-description}` | `chore/add-ruff-taskipy` |
| Refactor | `refactor/{short-description}` | `refactor/security-module` |

### Commit Messages

Follow Conventional Commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code restructuring |
| `chore` | Maintenance, deps, build |
| `test` | Adding tests |

**Examples:**
```
feat(auth): add refresh token endpoint
fix(books): prevent duplicate ISBN on update
docs: add mkdocs configuration
chore: add ruff and taskipy as dev dependencies
```

---

## Next Steps

- [Project Structure](project-structure.md)
