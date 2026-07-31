# System Architecture

High-level architecture diagrams and design documentation for the Library API.

---

## High-Level Architecture

```mermaid
graph TB
    Client[API Client\nBrowser, Mobile, CLI] -->|HTTPS/JSON| App[FastAPI Application\nUvicorn Workers]
    
    subgraph "Application Layer"
        App --> Router[API Routers\nAuth, Users, Authors, Books, Copies, Borrows]
        Router --> Deps[Dependencies\nDB Session, Auth, Permissions]
        Deps --> Core[Core Modules\nSecurity, Database, Settings]
        Core --> Models[SQLAlchemy Models\nUsers, Authors, Books, Copies, Borrows]
        Models --> DB[(Database\nPostgreSQL/SQLite)]
    end
    
    App --> Docs[OpenAPI 3.1\nSwagger UI / ReDoc]
    App --> Metrics[health_check]
```

---

## Component Architecture

```mermaid
graph LR
    subgraph "Presentation Layer"
        Routers[API Routers]
        Schemas[Pydantic Schemas]
    end
    
    subgraph "Business Logic Layer"
        Dependencies[FastAPI Dependencies]
        Security[Auth & Security]
        Permissions[RBAC Permissions]
    end
    
    subgraph "Data Access Layer"
        Models[SQLAlchemy Models]
        Database[Async Database]
        Migrations[Alembic Migrations]
    end
    
    subgraph "Configuration"
        Settings[Pydantic Settings]
        Env[Environment Variables]
    end
    
    Routers --> Dependencies
    Routers --> Schemas
    Dependencies --> Security
    Dependencies --> Permissions
    Dependencies --> Database
    Security --> Models
    Models --> Database
    Database --> Migrations
    Settings --> Env
```

---

## Request Processing Flow

```mermaid
sequenceDiagram
    participant Client
    participant Router as FastAPI Router
    participant Dep as Dependencies
    participant Security as Security Module
    participant DB as Database Session
    participant Model as SQLAlchemy Models
    
    Client->>Router: HTTP Request
    Router->>Dep: Resolve Dependencies
    Dep->>Security: get_current_user(token)
    Security->>Security: verify_token()
    Security->>DB: SELECT user WHERE id=sub
    DB-->>Security: User Model
    Security-->>Dep: Current User
    Dep->>Permissions: require_roles(roles)
    Permissions-->>Dep: Authorized User
    Dep-->>Router: Injected Dependencies
    Router->>Model: Business Logic (CRUD)
    Model->>DB: SQLAlchemy Queries
    DB-->>Model: Results
    Model-->>Router: Domain Objects
    Router->>Schemas: Serialize Response
    Schemas-->>Router: Pydantic Models
    Router-->>Client: JSON Response
```

---

## Database Architecture

```mermaid
graph TB
    subgraph "Application"
        Engine[AsyncEngine\ncreate_async_engine]
        SessionFactory[async_sessionmaker\nAsyncSessionLocal]
        Session[AsyncSession\nget_session]
    end
    
    subgraph "Database"
        Pool[Connection Pool]
        SQLite[(SQLite File)]
        Postgres[(PostgreSQL)]
    end
    
    Settings[Settings.DATABASE_URL] --> Engine
    Engine --> Pool
    Pool --> SQLite
    Pool --> Postgres
    SessionFactory --> Engine
    Session --> SessionFactory
    
    Models[SQLAlchemy Models] --> Session
    Migrations[Alembic] --> Engine
```

---

## Security Architecture

```mermaid
graph TB
    subgraph "Authentication"
        Login[POST /token]
        Refresh[POST /refresh_token]
        JWT[JWT Tokens\nHS256]
        Password[Argon2 Hashing\npwdlib]
    end
    
    subgraph "Authorization"
        TokenDep[HTTPBearer Dependency]
        CurrentUser[get_current_user]
        Roles[require_roles]
    end
    
    Login --> Password
    Login --> JWT
    Refresh --> JWT
    JWT --> TokenDep
    TokenDep --> CurrentUser
    CurrentUser --> Roles
    Roles --> Routers
```

### Token Flow

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant Server
    
    User->>Client: Email + Password
    Client->>Server: POST /token
    Server->>Server: Verify password (Argon2)
    Server->>Server: Create JWT (sub=user_id, exp=5min)
    Server-->>Client: {access_token, token_type}
    Client->>Server: GET /protected (Bearer token)
    Server->>Server: Verify JWT signature & exp
    Server->>Server: Load user from DB
    Server-->>Client: Protected resource
```

---

## API Layer Architecture

### Router Organization

```
library_api/routers/
├── auth.py              # Public: /token, /refresh_token
├── users.py             # Admin: CRUD users
├── authors.py           # Admin/Librarian: CRUD authors; All: read
├── books.py             # Admin/Librarian: CRUD books; All: read
├── book_copies.py       # Admin/Librian: CRUD copies; All: read
└── borrow_records.py    # All: borrow/return; Admin/Librarian: list/delete
```

---

## Next Steps

- [Data Models (ERD)](data-models-erd.md) - Database schema
