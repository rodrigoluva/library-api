# Configuration

Complete reference for all configuration options in the Library API project.

---

## Environment Variables

All configuration is managed through environment variables via **Pydantic Settings**. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

---

## Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string (SQLAlchemy async format) | `sqlite+aiosqlite:///./library.db` or `postgresql+asyncpg://user:pass@localhost/db` |
| `JWT_SECRET_KEY` | Secret key for signing JWT tokens (min 32 chars) | `your-super-secret-key-change-in-production` |

---

## Optional Variables

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm | `HS256`, `RS256` |
| `JWT_EXPIRATION_MINUTES` | `5` | Access token lifetime in minutes | `15`, `30`, `60` |

---

## Complete `.env` Example

### Development (SQLite)

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./library.db

# JWT Authentication
JWT_SECRET_KEY=dev-secret-key-change-in-production-minimum-32-characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

### Production (PostgreSQL)

```env
# Database
DATABASE_URL=postgresql+asyncpg://library_user:secure_password@localhost:5432/library_api

# JWT Authentication
JWT_SECRET_KEY=super-secure-random-key-at-least-32-chars-generated-by-openssl
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
```

### Docker/Container

```env
# Database (using Docker service name)
DATABASE_URL=postgresql+asyncpg://library_user:secure_password@postgres:5432/library_api

# JWT Authentication
JWT_SECRET_KEY=${JWT_SECRET_KEY}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
```

### Generate Production Secrets

```bash
# JWT Secret
openssl rand -base64 32
```

---

## Database URL Formats

| Database | Format | Example |
|----------|--------|---------|
| **SQLite (async)** | `sqlite+aiosqlite:///path/to/db` | `sqlite+aiosqlite:///./library.db` |
| **PostgreSQL (asyncpg)** | `postgresql+asyncpg://user:pass@host:port/db` | `postgresql+asyncpg://user:pass@localhost:5432/library_api` |

> **Note**: This project uses **async SQLAlchemy**, so the database driver must support async operations (aiosqlite, asyncpg).

---

## Security Configuration

### JWT Tokens

The API uses JWT (JSON Web Token) based authentication. Tokens are valid for 5 minutes by default, as defined by the `JWT_EXPIRATION_MINUTES` variable.

### Password Hashing

Passwords are stored using Argon2 hashing, a password hashing algorithm resistant to brute-force attacks.

---

## JWT Configuration Details

### Token Structure

```json
{
  "sub": "1",           // User ID (subject)
  "exp": 1699999999,    // Expiration timestamp (UTC)
  "iat": 1699999999     // Issued at timestamp (UTC)
}
```

### Algorithm Options

| Algorithm | Key Type | Use Case |
|-----------|----------|----------|
| `HS256` | Symmetric (shared secret) | Simple deployments, single service |
| `RS256` | Asymmetric (RSA key pair) | Microservices, distributed systems |
| `ES256` | Asymmetric (ECDSA) | High security, smaller keys |

> **Current Implementation**: Only `HS256` is supported. For RS256/ES256, modify `library_api/core/security.py`.

### Expiration Recommendations

| Environment | Access Token | Refresh Token |
|-------------|--------------|---------------|
| Development | 30-60 min | 7-30 days |
| Staging | 15-30 min | 7 days |
| Production | 5-15 min | 1-7 days |

> **Security Note**: Short access tokens (5-15 min) with refresh tokens provide better security. Current implementation only has access tokens.

---

## Settings Class Reference

The configuration is loaded in `library_api/core/settings.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_MINUTES: int = 5
```

### Accessing Settings

```python
from library_api.core.settings import Settings

settings = Settings()
print(settings.DATABASE_URL)
print(settings.JWT_SECRET_KEY)
```

> **Important**: `Settings()` is a singleton-like class. Each instantiation reads from `.env`. Use the module-level instance in `library_api/core/security.py`:
> ```python
> from library_api.core.settings import Settings
> settings = Settings()  # Single instance used throughout app
> ```

---

## Server Configuration

### FastAPI

The application is configured in `library_api/app.py` and can be started with different options:

```bash
# Development mode with auto-reload
poetry run fastapi dev library_api/app.py

# Production mode
poetry run uvicorn library_api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Configuration Parameters

- `--host`: IP address to listen on (default: 127.0.0.1)
- `--port`: Port to listen on (default: 8000)
- `--workers`: Number of workers (default: 1, useful only in production)
- `--reload`: Enables automatic reloading (development only)

---

## Alembic Configuration (Migrations)

The project uses Alembic for database migration management. The configuration file is located at `alembic.ini`.

To run migrations:

```bash
# Apply all pending migrations
poetry run alembic upgrade head

# Create a new migration
poetry run alembic revision --autogenerate -m "Migration description"

# Roll back the last migration
poetry run alembic downgrade -1
```

---

## Linter and Formatter Configuration

The project uses Ruff for linting and code formatting. The configurations are in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79
exclude = [
    # List of excluded directories
]

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
ignore = ['PLR2004', 'PLR0917', 'PLR0913']

[tool.ruff.format]
preview = true
quote-style = 'single'
```

To run the linter and formatter:

```bash
# Check for style issues
poetry run ruff check

# Automatically fix issues
poetry run ruff check --fix

# Format code
poetry run ruff format
```

---

## MkDocs Configuration

The documentation is generated using MkDocs Material. The configurations are in `mkdocs.yml`.

To serve the documentation locally:

```bash
poetry run mkdocs serve -a 127.0.0.1:8001
```

---

## Next Steps

- [Installation](installation.md)
- [API Endpoints](api-endpoints.md)
