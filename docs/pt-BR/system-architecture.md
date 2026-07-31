# Arquitetura do Sistema

Diagramas de arquitetura de alto nível e documentação de projeto da Library API.

---

```mermaid
graph TB
    Client[Cliente da API\nNavegador, Mobile, CLI] -->|HTTPS/JSON| App[Aplicação FastAPI\nWorkers Uvicorn]

    subgraph "Camada de Aplicação"
        App --> Router[Roteadores da API\nAutenticação, Usuários, Autores, Livros, Exemplares, Empréstimos]
        Router --> Deps[Dependências\nSessão do BD, Autenticação, Permissões]
        Deps --> Core[Módulos Principais\nSegurança, Banco de Dados, Configurações]
        Core --> Models[Modelos SQLAlchemy\nUsuários, Autores, Livros, Exemplares, Empréstimos]
        Models --> DB[(Banco de Dados\nPostgreSQL/SQLite)]
    end

    App --> Docs[OpenAPI 3.1\nSwagger UI / ReDoc]
    App --> Metrics[health_check]
```

---

## Arquitetura de Componentes

```mermaid
graph LR
    subgraph "Camada de Apresentação"
        Routers[Roteadores da API]
        Schemas[Schemas Pydantic]
    end

    subgraph "Camada de Lógica de Negócios"
        Dependencies[Dependências do FastAPI]
        Security[Autenticação e Segurança]
        Permissions[Permissões RBAC]
    end

    subgraph "Camada de Acesso a Dados"
        Models[Modelos SQLAlchemy]
        Database[Banco de Dados Assíncrono]
        Migrations[Migrações Alembic]
    end

    subgraph "Configuração"
        Settings[Configurações Pydantic]
        Env[Variáveis ​​de Ambiente]
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

## Fluxo de Processamento de Requisições

```mermaid
sequenceDiagram
    participant Client
    participant Router as Roteador FastAPI
    participant Dep as Dependências
    participant Security as Módulo de Segurança
    participant DB as Sessão do Banco de Dados
    participant Model as Modelos SQLAlchemy

    Client->>Router: Requisição HTTP
    Router->>Dep: Resolver Dependências
    Dep->>Security: get_current_user(token)
    Security->>Security: verify_token()
    Security->>DB: SELECT user WHERE id=sub
    DB-->>Security: Modelo de Usuário
    Security-->>Dep: Usuário Atual
    Dep->>Permissions: require_roles(roles)
    Permissions-->>Dep: Usuário Autorizado
    Dep-->>Router: Dependências Injetadas
    Router->>Model: Lógica de Negócio (CRUD)
    Model->>DB: Consultas SQLAlchemy
    DB-->>Model: Resultados
    Model-->>Router: Objetos de Domínio
    Router->>Schemas: Serializar Resposta
    Schemas-->>Router: Modelos Pydantic
    Router-->>Client: Resposta JSON
```

---

## Arquitetura do Banco de Dados

```mermaid
graph TB
    subgraph "Aplicação"
        Engine[AsyncEngine\ncreate_async_engine]
        SessionFactory[async_sessionmaker\nAsyncSessionLocal]
        Session[AsyncSession\nget_session]
    end

    subgraph "Banco de Dados"
        Pool[Pool de Conexões]
        SQLite[(Arquivo SQLite)]
        Postgres[(PostgreSQL)]
    end

    Settings[Settings.DATABASE_URL] --> Engine
    Engine --> Pool
    Pool --> SQLite
    Pool --> Postgres
    SessionFactory --> Engine
    Session --> SessionFactory

    Models[Modelos SQLAlchemy] --> Session
    Migrations[Alembic] --> Engine
```

---

## Arquitetura de Segurança

```mermaid
graph TB
    subgraph "Autenticação"
        Login[POST /token]
        Refresh[POST /refresh_token]
        JWT[Tokens JWT\nHS256]
        Password[Hashing Argon2\npwdlib]
    end

    subgraph "Autorização"
        TokenDep[Dependência HTTPBearer]
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

### Fluxo de Token

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant Server

    User->>Client: E-mail + Senha
    Client->>Server: POST /token
    Server->>Server: Verificar senha (Argon2)
    Server->>Server: Criar JWT (sub=user_id, exp=5min)
    Server-->>Client: {access_token, token_type}
    Client->>Server: GET /protected (Token Bearer)
    Server->>Server: Verificar assinatura e expiração do JWT
    Server->>Server: Carregar usuário do banco de dados
    Server-->>Client: Recurso protegido
```

---

## Arquitetura da Camada de API

### Organização dos Roteadores

```
library_api/routers/
├── auth.py              # Público: /token, /refresh_token
├── users.py             # Admin: CRUD de usuários
├── authors.py           # Admin/Bibliotecário: CRUD de autores; Todos: leitura
├── books.py             # Admin/Bibliotecário: CRUD de livros; Todos: leitura
├── book_copies.py       # Admin/Bibliotecário: CRUD de exemplares; Todos: leitura
└── borrow_records.py    # Todos: empréstimo/devolução; Admin/Bibliotecário: listar/excluir
```

---

## Próximos Passos

- [Modelos de Dados (ERD)](data-models-erd.md)