# Project Structure

Detailed directory layout and file organization for the Library API project.

---

## Root Directory

```
library-api/
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── alembic.ini            # Alembic migration config
├── LICENSE                # Project license
├── mkdocs.yml             # MkDocs documentation config
├── openapi.json           # Exported OpenAPI spec
├── poetry.lock            # Locked dependencies
├── pyproject.toml         # Project config (Poetry, Ruff, Taskipy)
├── README.md              # Project overview (EN)
├── README.pt-BR.md        # Project overview (pt-BR)
│
├── .git/                  # Git repository
├── .ruff_cache/           # Ruff cache
├── .vscode/               # VS Code settings
│
├── docs/                  # MkDocs documentation
│   ├── en/                # English documentation (EN)
│   └── pt-BR/             # Brazilian Portugues documentation (PT-BR)
│
├── library_api/           # Main application package
│   ├── __init__.py        # Package exports
│   ├── app.py             # FastAPI app factory
│   ├── cli.py             # Typer CLI commands
│   │
│   ├── core/              # Cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── database.py    # Async engine & session factory
│   │   ├── security.py    # Auth, JWT, password hashing
│   │   └── settings.py    # Pydantic Settings
│   │
│   ├── dependencies/      # FastAPI dependency injection
│   │   ├── __init__.py
│   │   └── permissions.py # Role-based access control
│   │
│   ├── models/            # SQLAlchemy ORM models
│   │   ├── __init__.py    # Exports: Base, User, Author, Book, BookCopy, BorrowRecord
│   │   ├── base.py        # DeclarativeBase
│   │   ├── users.py       # User model + UserRole enum
│   │   └── books.py       # Author, Book, BookCopy, BorrowRecord + BookStatus enum
│   │
│   ├── routers/           # API endpoints (controllers)
│   │   ├── __init__.py
│   │   ├── auth.py        # POST /token, POST /refresh_token
│   │   ├── users.py       # /api/v1/users/*
│   │   ├── authors.py     # /api/v1/authors/*
│   │   ├── books.py       # /api/v1/books/*
│   │   ├── book_copies.py # /api/v1/book-copies/*, /books/{id}/copies
│   │   └── borrow_records.py # /api/v1/borrow-records/*, /books/{id}/borrow|return
│   │
│   └── schemas/           # Pydantic v2 models (API contracts)
│       ├── __init__.py
│       ├── auth.py        # Token, LoginRequest
│       ├── users.py       # UserSchema, UserUpdateSchema, UserPublicSchema, UserListPublicSchema
│       ├── authors.py     # AuthorSchema, AuthorUpdateSchema, AuthorPublicSchema, AuthorListPublicSchema
│       ├── books.py       # BookSchema, BookUpdateSchema, BookPublicSchema, BookRelationshipPublicSchema, BookRelationshipListPublicSchema, BookListPublicSchema
│       ├── book_copies.py # BookCopyCreateSchema, BookCopyUpdateSchema, BookCopyPublicSchema, BookCopyCreateListPublicSchema, BookCopyListPublicSchema
│       └── borrow_records.py # BorrowRecordPublicSchema, BorrowRecordListSchema
│
├── migrations/            # Alembic database migrations
│   ├── env.py             # Migration environment (async)
│   ├── script.py.mako     # Migration template
│   └── versions/          # Migration scripts
│       ├── b9e0f87139b3_create_users_table.py
│       ├── d58754e7c566_create_authors_books_book_copies_and_borrow_records.py
│       └── 2f8a67030948_feat_add_users_role.py
│
└── tests/                 # Test suite
    ├── __init__.py
    ├── conftest.py        # Pytest fixtures (async client, db, auth)
    ├── test_auth.py
    ├── test_users.py
    ├── test_authors.py
    ├── test_books.py
    ├── test_book_copies.py
    └── test_borrow_records.py
```

---

## Package: `library_api`

### Entry Points

| File | Purpose |
|------|---------|
| `app.py` | FastAPI application factory, router registration |
| `cli.py` | Typer CLI for admin user management |

### Core Module (`library_api/core/`)

| File | Responsibility |
|------|----------------|
| `database.py` | Async SQLAlchemy engine, session factory, `get_session()` dependency |
| `security.py` | Password hashing (Argon2), JWT create/verify, user authentication, `get_current_user` dependency |
| `settings.py` | Pydantic Settings: `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRATION_MINUTES` |

### Dependencies (`library_api/dependencies/`)

| File | Responsibility |
|------|----------------|
| `permissions.py` | `require_roles(*UserRole)` dependency for RBAC |

### Models (`library_api/models/`)

| File | Models |
|------|--------|
| `base.py` | `Base` (DeclarativeBase) |
| `users.py` | `User`, `UserRole` enum |
| `books.py` | `Author`, `Book`, `BookCopy`, `BorrowRecord`, `BookStatus` enum |

### Routers (`library_api/routers/`)

| File | Prefix | Tags | Endpoints |
|------|--------|------|-----------|
| `auth.py` | `/api/v1` | authentication | `POST /token`, `POST /refresh_token` |
| `users.py` | `/api/v1/users` | users | `POST /`, `GET /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}` |
| `authors.py` | `/api/v1/authors` | authors | `POST /`, `GET /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}` |
| `books.py` | `/api/v1/books` | books | `POST /`, `GET /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}` |
| `book_copies.py` | `/api/v1` | book-copies | `POST /books/{id}/copies`, `GET /book-copies`, `GET /book-copies/{id}`, `PUT /book-copies/{id}`, `DELETE /book-copies/{id}` |
| `borrow_records.py` | `/api/v1` | borrow-records | `POST /books/{id}/borrow`, `POST /books/{id}/return`, `GET /borrow-records`, `GET /borrow-records/{id}`, `DELETE /borrow-records/{id}` |

### Schemas (`library_api/schemas/`)

| File | Schemas |
|------|---------|
| `auth.py` | `Token`, `LoginRequest` |
| `users.py` | `UserSchema`, `UserUpdateSchema`, `UserPublicSchema`, `UserListPublicSchema` |
| `authors.py` | `AuthorSchema`, `AuthorUpdateSchema`, `AuthorPublicSchema`, `AuthorRelationshipPublicSchema`, `AuthorListPublicSchema` |
| `books.py` | `BookSchema`, `BookUpdateSchema`, `BookPublicSchema`, `BookRelationshipPublicSchema`, `BookRelationshipListPublicSchema`, `BookListPublicSchema` |
| `book_copies.py` | `BookCopyCreateSchema`, `BookCopyUpdateSchema`, `BookCopyPublicSchema`, `BookCopyCreateListPublicSchema`, `BookCopyListPublicSchema` |
| `borrow_records.py` | `BorrowRecordPublicSchema`, `BorrowRecordListSchema` |

---

## Migrations (`migrations/`)

### Structure

```
migrations/
├── env.py                 # Async migration environment
├── script.py.mako         # Template for new revisions
└── versions/
    ├── b9e0f87139b3_create_users_table.py                    # Initial: users table
    ├── d58754e7c566_create_authors_books_book_copies_and_borrow_records.py  # Core library tables
    └── 2f8a67030948_feat_add_users_role.py                   # Add role column to users
```

---

## Tests (`tests/`)

### Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_auth.py             # Authentication tests
├── test_users.py            # User CRUD tests
├── test_authors.py          # Author CRUD tests
├── test_books.py            # Book CRUD tests
├── test_book_copies.py      # Book copy CRUD tests
└── test_borrow_records.py   # Borrow/return flow tests
```

---

## Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project metadata, dependencies, tool config (Ruff, Taskipy, Poetry) |
| `poetry.lock` | Locked dependency versions |
| `alembic.ini` | Alembic migration configuration |
| `mkdocs.yml` | MkDocs documentation site configuration |
| `.env.example` | Environment variable template |
| `.gitignore` | Git ignore patterns |
| `openapi.json` | Exported OpenAPI 3.1 specification |
| `README.md` | Project Overview |
| `LICENSE` | Project license |

---

## Next Steps

- [API Endpoints](api-endpoints.md)
- [Data Models (ERD)](data-models-erd.md)
