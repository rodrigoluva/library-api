# Library API

## Overview

Library API is a RESTful API for managing a library system. It provides endpoints to manage users, authors, books, book copies, and borrow records, enabling efficient catalog management and book lending workflows.

The API supports the complete lifecycle of library resources, including registering users and authors, maintaining the book catalog, tracking individual physical copies, and recording borrowing and return operations. It is designed with a clear, modular architecture and follows REST best practices.

## Core Features

- **Authentication & Authorization**: JWT-based auth with role-based access control (Admin, Librarian, Member).
- **User Management**: Registration, profile management, role assignment.
- **Author Management**: CRUD operations for authors with biographical data.
- **Book Management**: Full book lifecycle with ISBN validation and author relationships.
- **Book Copy Management**: Physical copy tracking with availability status.
- **Borrowing System**: Check-out/check-in with due dates, conflict prevention.
- **Borrow Records**: Complete borrowing history with filtering.

## Technology Stack

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

## Quick Start

```bash
# Clone and enter project
cd library-api

# Install dependencies (using Poetry)
poetry install

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and JWT_SECRET_KEY

# Run migrations
poetry run alembic upgrade head

# Create admin user
poetry run python -m library_api.cli create-admin-user

# Start development server
poetry run task run
# or: poetry run fastapi dev library_api/app.py
```
> If you don't have Poetry or Git installed. Check the [Prerequisites](docs/en/prerequisites.md) guide.

Access `http://localhost:8000/docs` for the interactive API documentation (Swagger UI). If you have any question check the documentation at `docs/`.

## Docker compose

If you have **Docker** installed, getting started is much simpler. After cloning the repository and creating the `.env` file, run the following command to start the **Library API** application, the **PostgreSQL** database, apply the database migrations, and launch the API documentation.

> [!warning]
> When using **Docker**, do not wrap values in the `.env` file with quotes. Docker reads environment variables as plain strings, and including quotes may lead to unexpected behavior.

```sh
docker compose up
```

Now you enter inside the container using:

```sh
docker exec -it libraryapi-app-1 sh
```

Then, run the command described in [Create Initial User Admin](docs/en/installation.md#create-initial-admin-user) to create the administrator account.

When running the application with Docker Compose, the API documentation is exposed on port **80**. Open your browser and navigate to `http://localhost` or `http://127.0.0.1` to access it.

## Kubernetes

Para informações sobre a implantação local usando **Kubernetes**, consulte [Implantação](docs/en/deployment.md#deployment).

---

## Quick Links

- **API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **API Documentation (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`
- **Health Check**: `http://localhost:8000/health_check`
- **MkDocs Site**: `poetry run task docs` → `http://localhost:8001`

---

## License

This project is licensed under the terms of the MIT license.
