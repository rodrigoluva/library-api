# API Endpoints

Complete reference for all Library API endpoints.

---

## Overview

| Base URL | `http://localhost:8000/api/v1` |
|----------|--------------------------------|
| Auth | Bearer Token (JWT) |
| Content-Type | `application/json` |
| Docs | Swagger UI: `/docs` • ReDoc: `/redoc` |

---

## Authentication Endpoints

### POST `/token` - Login

**Public endpoint** - No authentication required

```bash
curl -X POST http://localhost:8000/api/v1/token \
  -H "Content-Type: application/json" \
  -d '{"email": "user@library.com", "password": "password123"}'
```

**Request Body** (`LoginRequest`)
```json
{
  "email": "user@library.com",
  "password": "password123"
}
```

**Response** (`Token`) - 200 OK
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors**
- `401` - Incorrect email or password
- `422` - Validation error

---

### POST `/refresh_token` - Refresh Access Token

**Requires:** Valid access token (Bearer)

```bash
curl -X POST http://localhost:8000/api/v1/refresh_token \
  -H "Authorization: Bearer <access_token>"
```

**Response** (`Token`) - 200 OK
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors**
- `401` - Invalid or expired token

---

## User Endpoints

**Base Path:** `/api/v1/users`  
**Auth Required:** Yes (Bearer Token)  
**Roles:** Admin only (except POST /)

---

### POST `/` - Create User (Register)

**Public endpoint**

```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@library.com", "password": "password123"}'
```

**Request Body** (`UserSchema`)
```json
{
  "name": "John Doe",
  "email": "john@library.com",
  "password": "password123"
}
```

**Response** (`UserPublicSchema`) - 201 Created
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@library.com",
  "role": "member",
  "created_at": "2026-07-27T10:30:00",
  "updated_at": "2026-07-27T10:30:00"
}
```

**Errors**
- `400` - Email already registered
- `422` - Validation error (password min 4 chars)

---

### GET `/` - List Users

**Requires:** Admin role

```bash
curl -X GET "http://localhost:8000/api/v1/users/?offset=0&limit=100&search=john" \
  -H "Authorization: Bearer <admin_token>"
```

**Query Parameters**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `offset` | int | 0 | Records to skip |
| `limit` | int | 100 | Max records (1-100) |
| `search` | string | - | Search by name or email |

**Response** (`UserListPublicSchema`) - 200 OK
```json
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@library.com",
      "role": "member",
      "created_at": "2026-07-27T10:30:00",
      "updated_at": "2026-07-27T10:30:00"
    }
  ],
  "offset": 0,
  "limit": 100
}
```

**Errors**
- `401` - Not authenticated
- `403` - Not enough permissions (not Admin)
- `404` - No users found matching criteria

---

### GET `/{user_id}` - Get User by ID

**Requires:** Admin role

```bash
curl -X GET http://localhost:8000/api/v1/users/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Response** (`UserPublicSchema`) - 200 OK

**Errors**
- `401` - Not authenticated
- `403` - Not enough permissions
- `404` - User not found

---

### PUT `/{user_id}` - Update User

**Requires:** Admin role

```bash
curl -X PUT http://localhost:8000/api/v1/users/1 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated", "role": "librarian"}'
```

**Request Body** (`UserUpdateSchema`) - All fields optional
```json
{
  "name": "John Updated",
  "email": "new@email.com",
  "password": "newpassword",
  "role": "librarian"
}
```

**Response** (`UserPublicSchema`) - 200 OK

**Errors**
- `400` - Email already in use
- `401` - Not authenticated
- `403` - Not enough permissions
- `404` - User not found

---

### DELETE `/{user_id}` - Delete User

**Requires:** Admin role

```bash
curl -X DELETE http://localhost:8000/api/v1/users/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Response** - 204 No Content

**Errors**
- `401` - Not authenticated
- `403` - Not enough permissions
- `404` - User not found

---

## Author Endpoints

**Base Path:** `/api/v1/authors`  
**Auth Required:** Yes (Bearer Token)  
**Roles:** Admin, Librarian (create/update/delete) • All roles (read)

---

### POST `/` - Create Author

**Requires:** Admin or Librarian

```bash
curl -X POST http://localhost:8000/api/v1/authors/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "George Orwell", "bio": "English novelist...", "birthdate": "1903-06-25"}'
```

**Request Body** (`AuthorSchema`)
```json
{
  "name": "George Orwell",
  "bio": "English novelist, essayist, journalist and critic",
  "birthdate": "1903-06-25"
}
```

**Response** (`AuthorPublicSchema`) - 201 Created
```json
{
  "id": 1,
  "name": "George Orwell",
  "bio": "English novelist...",
  "birthdate": "1903-06-25",
  "created_at": "2026-07-27T10:30:00",
  "updated_at": "2026-07-27T10:30:00"
}
```

---

### GET `/` - List Authors

**Requires:** Admin, Librarian, or Member

```bash
curl -X GET "http://localhost:8000/api/v1/authors/?offset=0&limit=100&search=orwell" \
  -H "Authorization: Bearer <token>"
```

**Query Parameters**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `offset` | int | 0 | Records to skip |
| `limit` | int | 100 | Max records (1-100) |
| `search` | string | - | Search by name |

**Response** (`AuthorListPublicSchema`) - 200 OK
```json
{
  "authors": [
    {
      "id": 1,
      "name": "George Orwell",
      "bio": "English novelist...",
      "birthdate": "1903-06-25",
      "created_at": "2026-07-27T10:30:00",
      "updated_at": "2026-07-27T10:30:00"
    }
  ],
  "offset": 0,
  "limit": 100
}
```

---

### GET `/{author_id}` - Get Author by ID

**Requires:** Admin, Librarian, or Member

```bash
curl -X GET http://localhost:8000/api/v1/authors/1 \
  -H "Authorization: Bearer <token>"
```

**Response** (`AuthorPublicSchema`) - 200 OK

---

### PUT `/{author_id}` - Update Author

**Requires:** Admin or Librarian

```bash
curl -X PUT http://localhost:8000/api/v1/authors/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"bio": "Updated biography"}'
```

**Request Body** (`AuthorUpdateSchema`) - All fields optional

**Response** (`AuthorPublicSchema`) - 200 OK

---

### DELETE `/{author_id}` - Delete Author

**Requires:** Admin only

```bash
curl -X DELETE http://localhost:8000/api/v1/authors/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Response** - 204 No Content

---

## Book Endpoints

**Base Path:** `/api/v1/books`  
**Auth Required:** Yes (Bearer Token)  
**Roles:** Admin, Librarian (create/update/delete) • All roles (read)

---

### POST `/` - Create Book

**Requires:** Admin or Librarian

```bash
curl -X POST http://localhost:8000/api/v1/books/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "1984", "isbn": "9780451524935", "published_date": "1949-06-08", "author_id": 1}'
```

**Request Body** (`BookSchema`)
```json
{
  "title": "1984",
  "isbn": "9780451524935",
  "published_date": "1949-06-08",
  "author_id": 1
}
```

**Response** (`BookPublicSchema`) - 201 Created
```json
{
  "id": 1,
  "title": "1984",
  "author_id": 1,
  "isbn": "9780451524935",
  "published_date": "1949-06-08",
  "created_at": "2026-07-27T10:30:00",
  "updated_at": "2026-07-27T10:30:00"
}
```

**Errors**
- `400` - ISBN already in use
- `404` - Author not found

---

### GET `/` - List Books

**Requires:** Admin, Librarian, or Member

```bash
curl -X GET "http://localhost:8000/api/v1/books/?offset=0&limit=100&search=1984&author_id=1" \
  -H "Authorization: Bearer <token>"
```

**Query Parameters**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `offset` | int | 0 | Records to skip |
| `limit` | int | 100 | Max records (1-100) |
| `search` | string | - | Search by ISBN or title |
| `author_id` | string | - | Filter by author ID |

**Response** (`BookListPublicSchema`) - 200 OK
```json
{
  "books": [
    {
      "id": 1,
      "title": "1984",
      "author": {
        "id": 1,
        "name": "George Orwell"
      },
      "isbn": "9780451524935",
      "available_copies": 3,
      "published_date": "1949-06-08",
      "created_at": "2026-07-27T10:30:00",
      "updated_at": "2026-07-27T10:30:00"
    }
  ],
  "offset": 0,
  "limit": 100
}
```

---

### GET `/{book_id}` - Get Book by ID

**Requires:** Admin, Librarian, or Member

```bash
curl -X GET http://localhost:8000/api/v1/books/1 \
  -H "Authorization: Bearer <token>"
```

**Response** (`BookRelationshipListPublicSchema`) - 200 OK
```json
{
  "id": 1,
  "title": "1984",
  "author": {
    "id": 1,
    "name": "George Orwell"
  },
  "isbn": "9780451524935",
  "available_copies": 3,
  "published_date": "1949-06-08",
  "created_at": "2026-07-27T10:30:00",
  "updated_at": "2026-07-27T10:30:00"
}
```

---

### PUT `/{book_id}` - Update Book

**Requires:** Admin or Librarian

```bash
curl -X PUT http://localhost:8000/api/v1/books/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Nineteen Eighty-Four", "author_id": 1}'
```

**Request Body** (`BookUpdateSchema`) - All fields optional

**Response** (`BookPublicSchema`) - 200 OK

**Errors**
- `400` - ISBN already in use
- `404` - Book or Author not found

---

### DELETE `/{book_id}` - Delete Book

**Requires:** Admin only

```bash
curl -X DELETE http://localhost:8000/api/v1/books/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Response** - 204 No Content

---

## Book Copy Endpoints

**Base Paths:** 
- `/api/v1/books/{book_id}/copies` (create copies for a book)
- `/api/v1/book-copies` (list/get/update/delete copies)  
**Auth Required:** Yes (Bearer Token)  
**Roles:** Admin, Librarian (create/update/delete) • Admin, Librarian, Member (list/get)

---

### POST `/books/{book_id}/copies` - Create Book Copies

**Requires:** Admin or Librarian

```bash
curl -X POST http://localhost:8000/api/v1/books/1/copies \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}'
```

**Request Body** (`BookCopyCreateSchema`)
```json
{
  "quantity": 5
}
```

**Response** (`BookCopyCreateListPublicSchema`) - 200 OK
```json
{
  "copies": [
    {
      "id": 6,
      "book": {
        "id": 1,
        "title": "1984",
        "author": {"id": 1, "name": "George Orwell"},
        "isbn": "9780451524935",
        "published_date": "1949-06-08",
        "created_at": "2026-07-27T10:30:00",
        "updated_at": "2026-07-27T10:30:00"
      },
      "status": "available",
      "created_at": "2026-07-27T10:35:00",
      "updated_at": "2026-07-27T10:35:00"
    }
    // ... 4 more copies
  ],
  "quantity": 5
}
```

---

### GET `/book-copies` - List Book Copies

**Requires:** Admin, Librarian, or Member

```bash
curl -X GET "http://localhost:8000/api/v1/book-copies?offset=0&limit=100&book_id=1" \
  -H "Authorization: Bearer <token>"
```

**Query Parameters**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `offset` | int | 0 | Records to skip |
| `limit` | int | 100 | Max records (1-100) |
| `search` | string | - | Search by book title |
| `book_id` | int | - | Filter by book ID |

**Response** (`BookCopyListPublicSchema`) - 200 OK

---

### GET `/book-copies/{book_copy_id}` - Get Book Copy by ID

**Requires:** Admin, Librarian, or Member

```bash
curl -X GET http://localhost:8000/api/v1/book-copies/1 \
  -H "Authorization: Bearer <token>"
```

**Response** (`BookCopyPublicSchema`) - 200 OK

---

### PUT `/book-copies/{book_copy_id}` - Update Book Copy

**Requires:** Admin or Librarian

```bash
curl -X PUT http://localhost:8000/api/v1/book-copies/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "borrowed"}'
```

**Request Body** (`BookCopyUpdateSchema`)
```json
{
  "book_id": 2,
  "status": "borrowed"
}
```

**Response** (`BookCopyPublicSchema`) - 200 OK

---

### DELETE `/book-copies/{book_copy_id}` - Delete Book Copy

**Requires:** Admin only

```bash
curl -X DELETE http://localhost:8000/api/v1/book-copies/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Response** - 204 No Content

---

## Borrow Record Endpoints

**Base Paths:**
- `/api/v1/books/{book_id}/borrow` - Borrow a book
- `/api/v1/books/{book_id}/return` - Return a book
- `/api/v1/borrow-records` - List/get/delete borrow records

**Auth Required:** Yes (Bearer Token)  
**Roles:** 
- Borrow/Return: All roles (own records)
- List/Get/Delete: Admin, Librarian

---

### POST `/books/{book_id}/borrow` - Borrow Book

**Requires:** Admin, Librarian, or Member (own account)

```bash
curl -X POST http://localhost:8000/api/v1/books/1/borrow \
  -H "Authorization: Bearer <member_token>"
```

**Response** (`BorrowRecordPublicSchema`) - 201 Created
```json
{
  "id": 1,
  "user_id": 5,
  "book_copy_id": 3,
  "borrowed_at": "2026-07-27T10:30:00Z",
  "due_at": "2026-08-10T10:30:00Z",
  "returned_at": null,
  "created_at": "2026-07-27T10:30:00Z",
  "updated_at": "2026-07-27T10:30:00Z"
}
```

**Business Rules**
- User cannot borrow same book twice (active borrow exists)
- Requires at least one available copy
- Sets due date to 14 days from borrow
- Marks copy as `borrowed`

**Errors**
- `404` - Book not found
- `409` - Already have this book borrowed OR no available copies

---

### POST `/books/{book_id}/return` - Return Book

**Requires:** Admin, Librarian, or Member (own account)

```bash
curl -X POST http://localhost:8000/api/v1/books/1/return \
  -H "Authorization: Bearer <member_token>"
```

**Response** (`BorrowRecordPublicSchema`) - 200 OK
```json
{
  "id": 1,
  "user_id": 5,
  "book_copy_id": 3,
  "borrowed_at": "2026-07-27T10:30:00Z",
  "due_at": "2026-08-10T10:30:00Z",
  "returned_at": "2026-08-05T14:22:00Z",
  "created_at": "2026-07-27T10:30:00Z",
  "updated_at": "2026-08-05T14:22:00Z"
}
```

**Business Rules**
- Finds active borrow record for user + book
- Sets `returned_at` to current time
- Marks copy as `available`

**Errors**
- `404` - Book not found OR no active borrow record

---

### GET `/borrow-records` - List Borrow Records

**Requires:** Admin or Librarian

```bash
curl -X GET "http://localhost:8000/api/v1/borrow-records?offset=0&limit=100&user_id=5" \
  -H "Authorization: Bearer <admin_token>"
```

**Query Parameters**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `offset` | int | 0 | Records to skip |
| `limit` | int | 100 | Max records (1-100) |
| `user_id` | int | - | Filter by user ID |
| `book_copy_id` | int | - | Filter by book copy ID |

**Response** (`BorrowRecordListSchema`) - 200 OK

---

### GET `/borrow-records/{borrow_record_id}` - Get Borrow Record

**Requires:** Admin or Librarian

```bash
curl -X GET http://localhost:8000/api/v1/borrow-records/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Response** (`BorrowRecordPublicSchema`) - 200 OK

---

### DELETE `/borrow-records/{borrow_record_id}` - Delete Borrow Record

**Requires:** Admin only

```bash
curl -X DELETE http://localhost:8000/api/v1/borrow-records/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Response** - 204 No Content

---

## Health Check

### GET `/health_check`

**Public endpoint**

```bash
curl http://localhost:8000/health_check
```

**Response** - 200 OK
```json
{
  "status": "200 OK"
}
```

---

## Response Schemas Summary

| Schema | Used In |
|--------|---------|
| `Token` | `/token`, `/refresh_token` |
| `UserPublicSchema` | User CRUD responses |
| `UserListPublicSchema` | `GET /users` |
| `AuthorPublicSchema` | Author CRUD responses |
| `AuthorListPublicSchema` | `GET /authors` |
| `AuthorRelationshipPublicSchema` | Nested in Book responses |
| `BookPublicSchema` | Book create/update responses |
| `BookRelationshipListPublicSchema` | `GET /books`, `GET /books/{id}` |
| `BookListPublicSchema` | `GET /books` |
| `BookCopyPublicSchema` | Book copy CRUD responses |
| `BookCopyCreateListPublicSchema` | `POST /books/{id}/copies` |
| `BookCopyListPublicSchema` | `GET /book-copies` |
| `BorrowRecordPublicSchema` | Borrow/return responses, record CRUD |
| `BorrowRecordListSchema` | `GET /borrow-records` |

---

## Error Response Format

All errors follow FastAPI's standard format:

```json
{
  "detail": "Error message"
}
```

Or validation errors (422):
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

---

## Quick Reference Card

| Category | Endpoints |
|----------|-----------|
| **Auth** | `POST /token`, `POST /refresh_token` |
| **Users** | `POST /users`, `GET /users`, `GET /users/{id}`, `PUT /users/{id}`, `DELETE /users/{id}` |
| **Authors** | `POST /authors`, `GET /authors`, `GET /authors/{id}`, `PUT /authors/{id}`, `DELETE /authors/{id}` |
| **Books** | `POST /books`, `GET /books`, `GET /books/{id}`, `PUT /books/{id}`, `DELETE /books/{id}` |
| **Copies** | `POST /books/{id}/copies`, `GET /book-copies`, `GET /book-copies/{id}`, `PUT /book-copies/{id}`, `DELETE /book-copies/{id}` |
| **Borrows** | `POST /books/{id}/borrow`, `POST /books/{id}/return`, `GET /borrow-records`, `GET /borrow-records/{id}`, `DELETE /borrow-records/{id}` |
| **Health** | `GET /health_check` |

---

## Next Steps

- [Data Models (ERD)](data-models-erd.md)
