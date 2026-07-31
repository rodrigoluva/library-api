# Installation

This guide will walk you through the installation and initial configuration of the Library API.

## Clone Repository

First, clone the repository to your local machine:

```bash
git clone <REPOSITORY_URL>
cd library-api
```

If you already have the source code locally, navigate to the project directory:

```bash
cd /path/to/library-api
```

## Installing Dependencies

The project uses Poetry for dependency management. Install all dependencies with the command:

```bash
poetry install
```

If you want to install only the main dependencies (excluding development ones):

```bash
poetry install --no-dev
```

## Activating the Virtual Environment

To work with the virtual environment created by Poetry:

```bash
poetry shell
```

Alternatively, you can run commands within the virtual environment without activating it:

```bash
poetry run python script.py
```

## Environment Configuration

### 1. Copy Example Environment File

```bash
cp .env.example .env
```

### 2. Configure `.env` File

Edit `.env` with your settings:

```env
# Database Configuration
# Development (SQLite - no setup required)
DATABASE_URL=sqlite+aiosqlite:///./library.db

# Production (PostgreSQL with asyncpg)
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/library_api

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=5
```

### 3. Generate Secure JWT Secret

```bash
# Using OpenSSL
openssl rand -base64 32
```

For more information about the project configuration, see the [Project Configuration](configuration.md) guide.

## Database Setup

### Development (SQLite)

The project uses SQLite as the default database. To initialize the database, run the Alembic migrations:

```bash
# Run migrations - creates library.db automatically
poetry run alembic upgrade head
```

This will create the necessary tables in the database.

### Production (PostgreSQL)

```bash
# 1. Create database and user
sudo -u postgres psql -c "CREATE DATABASE library_api;"
sudo -u postgres psql -c "CREATE USER library_user WITH ENCRYPTED PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE library_api TO library_user;"

# 2. Update .env with PostgreSQL URL
# DATABASE_URL=postgresql+asyncpg://library_user:secure_password@localhost:5432/library_api

# 3. Run migrations
poetry run alembic upgrade head
```

### Verify Database

```bash
# Check migration status
poetry run alembic current

# View migration history
poetry run alembic history
```

## Create Initial Admin User

The CLI provides commands to create admin and librarian users:

```bash
# Create admin user (interactive prompts)
poetry run python -m library_api.cli create-admin-user

# Create librarian user (interactive prompts)
poetry run python -m library_api.cli create-librarian-user
```

**Example interaction:**
```
$ poetry run python -m library_api.cli create-admin-user
Name: Admin User
Email: admin@library.com
Password: ********
Password (repeat): ********
Created admin user admin@library.com with id 1
```

## Start Development Server

```bash
# Using Taskipy (defined in pyproject.toml)
poetry run task run

# Or directly with FastAPI CLI
poetry run fastapi dev library_api/app.py

# Or with uvicorn directly
poetry run uvicorn library_api.app:app --reload --host 0.0.0.0 --port 8000
```

### Server Output

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Verify Installation

### API Documentation

Open in browser:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Test Authentication

If you're using Swagger UI and have already created an admin user, navigate to the **Create Access Token** endpoint.

- Click **Try it out**.
- Enter the email and password of the admin user you created.
- Click **Execute**.

If the request is successful, the response will include an access token. Copy the token, then click **Authorize** at the top of the page. Paste the token into the **Value** field and click **Authorize** again.

You are now authenticated and can access all protected endpoints.

## Start Documentation Site

```bash
# Build and serve MkDocs site
poetry run task docs

# Or directly
poetry run mkdocs serve -a 127.0.0.1:8001
```

Open http://localhost:8001 in browser.

## Troubleshooting

### Python Version Error

Ensure you are using Python 3.13 or higher:

```bash
python --version
```

If you are using a different version, you can specify the version for Poetry:

```bash
poetry env use python3.13
poetry install
```

### Dependency Installation Failure

If errors occur during dependency installation, try clearing the Poetry cache:

```bash
poetry cache clear pypi --all
poetry install
```

### Reset Database (Development)

```bash
# Remove SQLite database
rm library.db

# Re-run migrations
poetry run alembic upgrade head

# Re-create admin user
poetry run python -m library_api.cli create-admin-user
```

---

## Next Steps

Now that the installation is complete, you can:

- Configure the necessary environment variables ([Project Configuration](configuration.md))
- Explore the API endpoints ([API Endpoints](api-endpoints.md))
