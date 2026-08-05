# Estrutura do Projeto

Layout detalhado de diretórios e organização de arquivos para o projeto da Library API.

---

## Diretório Raiz

```
library-api/
├── .env.example           # Modelo de variáveis ​​de ambiente
├── .gitignore             # Regras de exclusão do Git
├── alembic.ini            # Configuração de migrações do Alembic
├── LICENSE                # Licença do projeto
├── mkdocs.yml             # Configuração da documentação MkDocs
├── openapi.json           # Especificação OpenAPI exportada
├── poetry.lock            # Dependências travadas (lockfile)
├── pyproject.toml         # Configuração do projeto (Poetry, Ruff, Taskipy)
├── README.md              # Visão geral do projeto (EN)
├── README.pt-BR.md        # Visão geral do projeto (pt-BR)
│
├── .git/                  # Repositório Git
├── .ruff_cache/           # Cache do Ruff
├── .vscode/               # Configurações do VS Code
│
├── docs/                  # Documentação MkDocs
│   ├── en/                # Documentação em inglês (EN)
│   └── pt-BR/             # Documentação em português brasileiro (PT-BR)
│
├── library_api/           # Pacote principal da aplicação
│   ├── __init__.py        # Exportações do pacote
│   ├── app.py             # Fábrica da aplicação FastAPI
│   ├── cli.py             # Comandos CLI do Typer
│   │
│   ├── core/              # Funcionalidades transversais (cross-cutting concerns)
│   │   ├── __init__.py
│   │   ├── database.py    # Engine assíncrona e fábrica de sessões
│   │   ├── security.py    # Autenticação, JWT, hashing de senha
│   │   └── settings.py    # Configurações Pydantic
│   │
│   ├── dependencies/      # Injeção de dependência do FastAPI
│   │   ├── __init__.py
│   │   └── permissions.py # Controle de acesso baseado em funções (RBAC)
│   │
│   ├── models/            # Modelos ORM do SQLAlchemy
│   │   ├── __init__.py    # Exportações: Base, User, Author, Book, BookCopy, BorrowRecord
│   │   ├── base.py        # DeclarativeBase
│   │   ├── users.py       # Modelo User + enum UserRole
│   │   └── books.py       # Author, Book, BookCopy, BorrowRecord + enum BookStatus
│   │
│   ├── routers/           # Endpoints da API (controllers)
│   │   ├── __init__.py
│   │   ├── auth.py        # POST /token, POST /refresh_token
│   │   ├── users.py       # /api/v1/users/*
│   │   ├── authors.py     # /api/v1/authors/*
│   │   ├── books.py       # /api/v1/books/*
│   │   ├── book_copies.py # /api/v1/book-copies/*, /books/{id}/copies
│   │   └── borrow_records.py # /api/v1/borrow-records/*, /books/{id}/borrow|return
│   │
│   └── schemas/           # Modelos Pydantic v2 (contratos da API)
│       ├── __init__.py
│       ├── auth.py        # Token, LoginRequest
│       ├── users.py       # UserSchema, UserUpdateSchema, UserPublicSchema, UserListPublicSchema
│       ├── authors.py     # AuthorSchema, AuthorUpdateSchema, AuthorPublicSchema, AuthorListPublicSchema
│       ├── books.py       # BookSchema, BookUpdateSchema, BookPublicSchema, BookRelationshipPublicSchema, BookRelationshipListPublicSchema, BookListPublicSchema
│       ├── book_copies.py # BookCopyCreateSchema, BookCopyUpdateSchema, BookCopyPublicSchema, BookCopyCreateListPublicSchema, BookCopyListPublicSchema
│       └── borrow_records.py # BorrowRecordPublicSchema, BorrowRecordListSchema
│
├── migrations/            # Migrações de banco de dados com Alembic
│   ├── env.py             # Ambiente de migração (assíncrono)
│   ├── script.py.mako     # Template de migração
│   └── versions/          # Scripts de migração
│       ├── b9e0f87139b3_create_users_table.py
│       ├── d58754e7c566_create_authors_books_book_copies_and_borrow_records.py
│       └── 2f8a67030948_feat_add_users_role.py
│
└── tests/                 # Pasta de testes
├── __init__.py
├── conftest.py        # Fixtures do Pytest (cliente assíncrono, banco de dados, autenticação)
├── test_auth.py
├── test_users.py
├── test_authors.py
├── test_books.py
├── test_book_copies.py
└── test_borrow_records.py
```

---

## Pacote: `library_api`

### Pontos de Entrada

| Arquivo | Finalidade |
|------|---------|
| `app.py` | Fábrica da aplicação FastAPI, registro de rotas |
| `cli.py` | CLI (Typer) para gerenciamento de usuários administradores |

### Módulo Principal (`library_api/core/`)

| Arquivo | Responsabilidade |
|------|----------------|
| `database.py` | Engine assíncrono do SQLAlchemy, fábrica de sessões, dependência `get_session()` |
| `security.py` | Hashing de senhas (Argon2), criação/verificação de JWT, autenticação de usuários, dependência `get_current_user` |
| `settings.py` | Configurações Pydantic: `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRATION_MINUTES` |

### Dependências (`library_api/dependencies/`)

| Arquivo | Responsabilidade |
|------|----------------|
| `permissions.py` | Dependência `require_roles(*UserRole)` para RBAC |

### Modelos (`library_api/models/`)

| Arquivo | Modelos |
|------|--------|
| `base.py` | `Base` (DeclarativeBase) |
| `users.py` | `User`, enum `UserRole` |
| `books.py` | `Author`, `Book`, `BookCopy`, `BorrowRecord`, enum `BookStatus` |

### Roteadores (`library_api/routers/`)

| Arquivo | Prefixo | Tags | Endpoints |
|------|--------|------|-----------|
| `auth.py` | `/api/v1` | authentication | `POST /token`, `POST /refresh_token` |
| `users.py` | `/api/v1/users` | users | `POST /`, `GET /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}` |
| `authors.py` | `/api/v1/authors` | authors | `POST /`, `GET /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}` |
| `books.py` | `/api/v1/books` | books | `POST /`, `GET /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}` |
| `book_copies.py` | `/api/v1` | book-copies | `POST /books/{id}/copies`, `GET /book-copies`, `GET /book-copies/{id}`, `PUT /book-copies/{id}`, `DELETE /book-copies/{id}` |
| `borrow_records.py` | `/api/v1` | borrow-records | `POST /books/{id}/borrow`, `POST /books/{id}/return`, `GET /borrow-records`, `GET /borrow-records/{id}`, `DELETE /borrow-records/{id}` |

### Schemas (`library_api/schemas/`)

| Arquivo | Schemas |
|---------|---------|
| `auth.py` | `Token`, `LoginRequest` |
| `users.py` | `UserSchema`, `UserUpdateSchema`, `UserPublicSchema`, `UserListPublicSchema` |
| `authors.py` | `AuthorSchema`, `AuthorUpdateSchema`, `AuthorPublicSchema`, `AuthorRelationshipPublicSchema`, `AuthorListPublicSchema` |
| `books.py` | `BookSchema`, `BookUpdateSchema`, `BookPublicSchema`, `BookRelationshipPublicSchema`, `BookRelationshipListPublicSchema`, `BookListPublicSchema` |
| `book_copies.py` | `BookCopyCreateSchema`, `BookCopyUpdateSchema`, `BookCopyPublicSchema`, `BookCopyCreateListPublicSchema`, `BookCopyListPublicSchema` |
| `borrow_records.py` | `BorrowRecordPublicSchema`, `BorrowRecordListSchema` ||

---

## Migrações (`migrations/`)

### Estrutura

```
migrations/
├── env.py                 # Ambiente de migração assíncrona
├── script.py.mako         # Modelo para novas revisões
└── versions/
├── b9e0f87139b3_create_users_table.py                    # Inicial: tabela de usuários
├── d58754e7c566_create_authors_books_book_copies_and_borrow_records.py  # Tabelas principais da biblioteca
└── 2f8a67030948_feat_add_users_role.py                   # Adição da coluna de função (role) aos usuários
```

---

## Testes (`tests/`)

### Estrutura

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartilhadas
├── test_auth.py             # Testes de autenticação
├── test_users.py            # Testes de CRUD de usuários
├── test_authors.py          # Testes de CRUD de autores
├── test_books.py            # Testes de CRUD de livros
├── test_book_copies.py      # Testes de CRUD de exemplares de livros
└── test_borrow_records.py   # Testes de fluxo de empréstimo/devolução
```

---

## Arquivos de Configuração

| Arquivo | Finalidade |
|------|---------|
| `pyproject.toml` | Metadados do projeto, dependências, configuração de ferramentas (Ruff, Taskipy, Poetry) |
| `poetry.lock` | Versões fixas das dependências |
| `alembic.ini` | Configuração de migrações do Alembic |
| `mkdocs.yml` | Configuração do site de documentação MkDocs |
| `.env.example` | Modelo de variáveis ​​de ambiente |
| `.gitignore` | Padrões de ignorar do Git |
| `openapi.json` | Especificação OpenAPI 3.1 exportada |
| `README.md` | Visáo geral do projeto |
| `LICENSE` | Licença do projeto |

---

## Próximos Passos

- [Endpoints da API](api-endpoints.md)
- [Modelos de Dados (ERD)](data-models-erd.md)
