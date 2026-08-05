# Library API Documentation

## Project Overview

The **Library API** is a modern, asynchronous RESTful API built with **FastAPI** to manage a library system. It offers comprehensive functionality for managing users, authors, books, book copies, and loan records, featuring role-based access control (RBAC).

### Core Features

- **Authentication & Authorization**: JWT-based auth with role-based access control (Admin, Librarian, Member).
- **User Management**: Registration, profile management, role assignment.
- **Author Management**: CRUD operations for authors with biographical data.
- **Book Management**: Full book lifecycle with ISBN validation and author relationships.
- **Book Copy Management**: Physical copy tracking with availability status.
- **Borrowing System**: Check-out/check-in with due dates, conflict prevention.
- **Borrow Records**: Complete borrowing history with filtering.

### Technology Stack

- **Python**: 3.13+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (Async)
- **Validation**: Pydantic V2
- **Database**: PostgreSQL (production) / SQLite (dev)
- **Migrations**: Alembic
- **Auth**: JWT (PyJWT) + Argon2 (pwdlib)
- **CLI**: Typer
- **Docs**: MkDocs + OpenAPI 3.1
- **Linting**: Ruff

### Architecture Highlights

- **Async-first** design with `async/await` throughout
- **Clean architecture** separation: routers → schemas → models → core
- **Dependency injection** for database sessions and auth
- **Role-based permissions** via FastAPI dependencies
- **Database migrations** with Alembic (async support)
- **OpenAPI 3.1** specification auto-generated
- **Type-safe** with full Pydantic v2 validation

---

## Starting

To start using this API, follow the steps described in the [Installation](installation.md) section. The API is ready to be integrated with front-end applications or used directly via HTTP requests.

### Documentation Structure

Explore the sections below for detailed information on all aspects of the API:

- [Prerequisites](prerequisites.md)
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Guidelines](guidelines.md)
- [Project Structure](project-structure.md)
- [API Endpoints](api-endpoints.md)
- [Data Models (ERD)](data-models-erd.md)
- [System Architecture](system-architecture.md)
- [Tests](tests.md)
- [Deployment](deployment.md)


---

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

---

## Author

**Rodrigo Valladão** - [rodrigoluva@gmail.com](mailto:rodrigoluva@gmail.com)
