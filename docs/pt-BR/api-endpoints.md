# Endpoints da API

Referência completa de todos os endpoints da Library API.

---

## Visão Geral

| Base URL | `http://localhost:8000/api/v1` |
|----------|--------------------------------|
| Auth | Bearer Token (JWT) |
| Content-Type | `application/json` |
| Docs | Swagger UI: `/docs` • ReDoc: `/redoc` |

---

## Endpoints de Autenticação

### POST `/token` - Login

**Endpoint público** - Não requer autenticação

```bash
curl -X POST http://localhost:8000/api/v1/token \
  -H "Content-Type: application/json" \
  -d '{"email": "user@library.com", "password": "password123"}'
```

**Corpo da Requisição** (`LoginRequest`)
```json
{
  "email": "user@library.com",
  "password": "password123"
}
```

**Resposta** (`Token`) - 200 OK
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erros**
- `401` - E-mail ou senha incorretos
- `422` - Erro de validação
---

### POST `/refresh_token` - Renovar Token de Acesso

**Requer:** Token de acesso válido (Bearer)

```bash
curl -X POST http://localhost:8000/api/v1/refresh_token \
  -H "Authorization: Bearer <access_token>"
```

**Resposta** (`Token`) - 200 OK
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erros**
- `401` - Token inválido ou expirado

---

## Endpoints de Usuário

**Caminho Base:** `/api/v1/users`  
**Autenticação Necessária:** Sim (Token Bearer)  
**Funções:** Apenas Admin (exceto POST /)

---

### POST `/` - Criar Usuário (Cadastro)

**Endpoint público**

```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@library.com", "password": "password123"}'
```

**Corpo da Requisição** (`UserSchema`)
```json
{
  "name": "John Doe",
  "email": "john@library.com",
  "password": "password123"
}
```

**Resposta** (`UserPublicSchema`) - 201 Created
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

**Erros**
- `400` - E-mail já cadastrado
- `422` - Erro de validação (senha com no mínimo 4 caracteres)

---

### GET `/` - Listar Usuários

**Requisito:** Função de administrador (Admin)

```bash
curl -X GET "http://localhost:8000/api/v1/users/?offset=0&limit=100&search=john" \
-H "Authorization: Bearer <admin_token>"
```

**Parâmetros de Consulta**

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-----------|
| `offset` | int | 0 | Registros a pular |
| `limit` | int | 100 | Máximo de registros (1-100) |
| `search` | string | - | Busca por nome ou e-mail |

**Resposta** (`UserListPublicSchema`) - 200 OK
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

**Erros**
- `401` - Não autenticado
- `403` - Permissões insuficientes (não é Admin)
- `404` - Nenhum usuário encontrado com os critérios informados

---

### GET `/{user_id}` - Obter usuário pelo ID

**Requisito:** Função de administrador

```bash
curl -X GET http://localhost:8000/api/v1/users/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Resposta** (`UserPublicSchema`) - 200 OK

**Erros**
- `401` - Não autenticado
- `403` - Permissões insuficientes
- `404` - Usuário não encontrado

---

### PUT `/{user_id}` - Atualizar Usuário

**Requisito:** Função de administrador

```bash
curl -X PUT http://localhost:8000/api/v1/users/1 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated", "role": "librarian"}'
```

**Corpo da Requisição** (`UserUpdateSchema`) - Todos os campos são opcionais
```json
{
  "name": "John Updated",
  "email": "new@email.com",
  "password": "newpassword",
  "role": "librarian"
}
```

**Resposta** (`UserPublicSchema`) - 200 OK

**Erros**
- `400` - E-mail já em uso
- `401` - Não autenticado
- `403` - Permissões insuficientes
- `404` - Usuário não encontrado

---

### DELETE `/{user_id}` - Excluir Usuário

**Requisito:** Função de administrador

```bash
curl -X DELETE http://localhost:8000/api/v1/users/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Resposta** - 204 No Content

**Erros**
- `401` - Não autenticado
- `403` - Permissões insuficientes
- `404` - Usuário não encontrado

---

## Endpoints de Autores

**Caminho Base:** `/api/v1/authors`  
**Autenticação Necessária:** Sim (Token Bearer)  
**Funções:** Admin, Bibliotecário (criar/atualizar/excluir) • Todas as funções (leitura)

---

### POST `/` - Criar Autor

**Requer:** Administrador ou Bibliotecário

```bash
curl -X POST http://localhost:8000/api/v1/authors/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "George Orwell", "bio": "English novelist...", "birthdate": "1903-06-25"}'
```

**Corpo da Requisição** (`AuthorSchema`)
```json
{
  "name": "George Orwell",
  "bio": "English novelist, essayist, journalist and critic",
  "birthdate": "1903-06-25"
}
```

**Resposta** (`AuthorPublicSchema`) - 201 Created
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

### GET `/` - Listar Autores

**Requer:** Administrador, Bibliotecário ou Membro

```bash
curl -X GET "http://localhost:8000/api/v1/authors/?offset=0&limit=100&search=orwell" \
  -H "Authorization: Bearer <token>"
```

**Parâmetros de Consulta**

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-------------|
| `offset` | int | 0 | Registros a pular |
| `limit` | int | 100 | Máximo de registros (1-100) |
| `search` | string | - | Busca por nome |

**Resposta** (`AuthorListPublicSchema`) - 200 OK
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

### GET `/{author_id}` - Obter Autor por ID

**Requer:** Administrador, Bibliotecário ou Membro

```bash
curl -X GET http://localhost:8000/api/v1/authors/1 \
  -H "Authorization: Bearer <token>"
```

**Resposta** (`AuthorPublicSchema`) - 200 OK

---

### PUT `/{author_id}` - Atualizar Autor

**Requer:** Administrador ou Bibliotecário

```bash
curl -X PUT http://localhost:8000/api/v1/authors/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"bio": "Updated biography"}'
```

**Corpo da Requisição** (`AuthorUpdateSchema`) - Todos os campos são opcionais

**Resposta** (`AuthorPublicSchema`) - 200 OK

---

### DELETE `/{author_id}` - Excluir Autor

**Requisito:** Apenas administrador

```bash
curl -X DELETE http://localhost:8000/api/v1/authors/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Resposta** - 204 No Content

---

## Endpoints de Livros

**Caminho Base:** `/api/v1/books`  
**Autenticação Necessária:** Sim (Token Bearer)  
**Funções:** Admin, Bibliotecário (criar/atualizar/excluir) • Todas as funções (leitura)

---

### POST `/` - Criar Livro

**Requer:** Administrador ou Bibliotecário

```bash
curl -X POST http://localhost:8000/api/v1/books/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "1984", "isbn": "9780451524935", "published_date": "1949-06-08", "author_id": 1}'
```

**Corpo da Requisição** (`BookSchema`)
```json
{
  "title": "1984",
  "isbn": "9780451524935",
  "published_date": "1949-06-08",
  "author_id": 1
}
```

**Resposta** (`BookPublicSchema`) - 201 Created
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

**Erros**
- `400` - ISBN já em uso
- `404` - Autor não encontrado

---

### GET `/` - Listar Livros

**Requer:** Administrador, Bibliotecário ou Membro

```bash
curl -X GET "http://localhost:8000/api/v1/books/?offset=0&limit=100&search=1984&author_id=1" \
  -H "Authorization: Bearer <token>"
```

**Parâmetros de Consulta**

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-------------|
| `offset` | int | 0 | Registros a pular |
| `limit` | int | 100 | Máximo de registros (1-100) |
| `search` | string | - | Busca por ISBN ou título |
| `author_id` | string | - | Filtro pelo ID do autor |

**Resposta** (`BookListPublicSchema`) - 200 OK
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

### GET `/{book_id}` - Obter livro pelo ID

**Requer:** Administrador, Bibliotecário ou Membro

```bash
curl -X GET http://localhost:8000/api/v1/books/1 \
-H "Authorization: Bearer <token>"
```

**Resposta** (`BookRelationshipListPublicSchema`) - 200 OK
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

### PUT `/{book_id}` - Atualizar Livro

**Requer:** Administrador ou Bibliotecário

```bash
curl -X PUT http://localhost:8000/api/v1/books/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Nineteen Eighty-Four", "author_id": 1}'
```

**Corpo da Requisição** (`BookUpdateSchema`) - Todos os campos são opcionais

**Resposta** (`BookPublicSchema`) - 200 OK

**Erros**
- `400` - ISBN já em uso
- `404` - Livro ou Autor não encontrado

---

### DELETE `/{book_id}` - Excluir Livro

**Requisito:** Apenas administrador

```bash
curl -X DELETE http://localhost:8000/api/v1/books/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Resposta** - 204 No Content

---

## Endpoints de Exemplares de Livros

**Caminhos Base:**
- `/api/v1/books/{book_id}/copies` (criar exemplares para um livro)
- `/api/v1/book-copies` (listar/obter/atualizar/excluir exemplares)  
**Autenticação Necessária:** Sim (Bearer Token)
**Papéis:** Admin, Bibliotecário (criar/atualizar/excluir) • Admin, Bibliotecário, Membro (listar/obter)

---

### POST `/books/{book_id}/copies` - Criar Exemplares de Livro

**Requer:** Administrador ou Bibliotecário

```bash
curl -X POST http://localhost:8000/api/v1/books/1/copies \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}'
```

**Corpo da Requisição** (`BookCopyCreateSchema`)
```json
{
  "quantity": 5
}
```

**Resposta** (`BookCopyCreateListPublicSchema`) - 200 OK
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
    // ... mais 4 exemplares
  ],
  "quantity": 5
}
```

---

### GET `/book-copies` - Listar Exemplares de Livros

**Requer:** Administrador, Bibliotecário ou Membro

```bash
curl -X GET "http://localhost:8000/api/v1/book-copies?offset=0&limit=100&book_id=1" \
  -H "Authorization: Bearer <token>"
```

**Parâmetros de Consulta**

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-----------|
| `offset` | int | 0 | Registros a pular |
| `limit` | int | 100 | Máximo de registros (1-100) |
| `search` | string | - | Pesquisar pelo título do livro |
| `book_id` | int | - | Filtrar pelo ID do livro |

**Resposta** (`BookCopyListPublicSchema`) - 200 OK

---

### GET `/book-copies/{book_copy_id}` - Obter exemplar de livro pelo ID

**Requer:** Administrador, Bibliotecário ou Membro

```bash
curl -X GET http://localhost:8000/api/v1/book-copies/1 \
  -H "Authorization: Bearer <token>"
```

**Resposta** (`BookCopyPublicSchema`) - 200 OK

---

### PUT `/book-copies/{book_copy_id}` - Atualizar Exemplar de Livro

**Requer:** Administrador ou Bibliotecário

```bash
curl -X PUT http://localhost:8000/api/v1/book-copies/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "borrowed"}'
```

**Corpo da Requisição** (`BookCopyUpdateSchema`)
```json
{
  "book_id": 2,
  "status": "borrowed"
}
```

**Resposta** (`BookCopyPublicSchema`) - 200 OK

---

### DELETE `/book-copies/{book_copy_id}` - Excluir Exemplar de Livro

**Requisito:** Apenas administrador

```bash
curl -X DELETE http://localhost:8000/api/v1/book-copies/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Resposta** - 204 No Content

---

## Endpoints de Registros de Empréstimo

**Caminhos Base:**
- `/api/v1/books/{book_id}/borrow` - Empréstimo de livro
- `/api/v1/books/{book_id}/return` - Devolução de livro
- `/api/v1/borrow-records` - Listar/obter/excluir registros de empréstimo  
**Autenticação Necessária:** Sim (Token Bearer)  
**Funções:**
- Empréstimo/Devolução: Todas as funções (registros próprios)
- Listar/Obter/Excluir: Administrador, Bibliotecário

---

### POST `/books/{book_id}/borrow` - Empréstimo de Livro

**Requer:** Administrador, Bibliotecário ou Membro (conta própria)

```bash
curl -X POST http://localhost:8000/api/v1/books/1/borrow \
  -H "Authorization: Bearer <member_token>"
```

**Resposta** (`BorrowRecordPublicSchema`) - 201 Created
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

**Regras de Negócio**
- O usuário não pode pegar o mesmo livro emprestado duas vezes (se já houver um empréstimo ativo)
- Requer pelo menos um exemplar disponível
- Define a data de devolução para 14 dias após o empréstimo
- Marca o exemplar como `borrowed` (emprestado)

**Erros**
- `404` - Livro não encontrado
- `409` - Já possui este livro emprestado OU não há exemplares disponíveis

---

### POST `/books/{book_id}/return` - Devolver Livro

**Requer:** Administrador, Bibliotecário ou Membro (conta própria)

```bash
curl -X POST http://localhost:8000/api/v1/books/1/return \
  -H "Authorization: Bearer <member_token>"
```

**Resposta** (`BorrowRecordPublicSchema`) - 200 OK
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

**Regras de Negócio**
- Localiza o registro de empréstimo ativo para o usuário + livro
- Define `returned_at` como o horário atual
- Marca o exemplar como `available` (disponível)

**Erros**
- `404` - Livro não encontrado OU nenhum registro de empréstimo ativo

---

### GET `/borrow-records` - Listar Registros de Empréstimo

**Requer:** Administrador ou Bibliotecário

```bash
curl -X GET "http://localhost:8000/api/v1/borrow-records?offset=0&limit=100&user_id=5" \
  -H "Authorization: Bearer <admin_token>"
```

**Parâmetros de Consulta**

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-------------|
| `offset` | int | 0 | Registros a pular |
| `limit` | int | 100 | Máximo de registros (1-100) |
| `user_id` | int | - | Filtrar pelo ID do usuário |
| `book_copy_id` | int | - | Filtrar pelo ID do exemplar do livro |

**Resposta** (`BorrowRecordListSchema`) - 200 OK

---

### GET `/borrow-records/{borrow_record_id}` - Obter Registro de Empréstimo

**Requer:** Administrador ou Bibliotecário

```bash
curl -X GET http://localhost:8000/api/v1/borrow-records/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Resposta** (`BorrowRecordPublicSchema`) - 200 OK

---

### DELETE `/borrow-records/{borrow_record_id}` - Excluir Registro de Empréstimo

**Requisito:** Apenas administrador

```bash
curl -X DELETE http://localhost:8000/api/v1/borrow-records/1 \
  -H "Authorization: Bearer <admin_token>"
```

**Resposta** - 204 No Content

---

## Health Check

### GET `/health_check`

**Endpoint público**

```bash
curl http://localhost:8000/health_check
```

**Resposta** - 200 OK
```json
{
  "status": "200 OK"
}
```

---

## Resumo dos Esquemas de Resposta

| Esquema | Utilizado em |
|--------|---------|
| `Token` | `/token`, `/refresh_token` |
| `UserPublicSchema` | Respostas de CRUD de usuário |
| `UserListPublicSchema` | `GET /users` |
| `AuthorPublicSchema` | Respostas de CRUD de autor |
| `AuthorListPublicSchema` | `GET /authors` |
| `AuthorRelationshipPublicSchema` | Aninhado em respostas de livro |
| `BookPublicSchema` | Respostas de criação/atualização de livro |
| `BookRelationshipListPublicSchema` | `GET /books`, `GET /books/{id}` |
| `BookListPublicSchema` | `GET /books` |
| `BookCopyPublicSchema` | Respostas de CRUD de exemplar de livro |
| `BookCopyCreateListPublicSchema` | `POST /books/{id}/copies` |
| `BookCopyListPublicSchema` | `GET /book-copies` |
| `BorrowRecordPublicSchema` | Respostas de empréstimo/devolução, CRUD de registro |
| `BorrowRecordListSchema` | `GET /borrow-records` |

---

## Formato de Resposta de Erro

Todos os erros seguem o formato padrão do FastAPI:

```json
{
  "detail": "Mensagem de erro"
}
```

Ou erros de validação (422):
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Campo obrigatório",
      "type": "missing"
    }
  ]
}
```

---

## Cartão de Referência Rápida

| Categoria | Endpoints |
|----------|-----------|
| **Autenticação** | `POST /token`, `POST /refresh_token` |
| **Usuários** | `POST /users`, `GET /users`, `GET /users/{id}`, `PUT /users/{id}`, `DELETE /users/{id}` |
| **Autores** | `POST /authors`, `GET /authors`, `GET /authors/{id}`, `PUT /authors/{id}`, `DELETE /authors/{id}` |
| **Livros** | `POST /books`, `GET /books`, `GET /books/{id}`, `PUT /books/{id}`, `DELETE /books/{id}` |
| **Exemplares** | `POST /books/{id}/copies`, `GET /book-copies`, `GET /book-copies/{id}`, `PUT /book-copies/{id}`, `DELETE /book-copies/{id}` |
| **Empréstimos** | `POST /books/{id}/borrow`, `POST /books/{id}/return`, `GET /borrow-records`, `GET /borrow-records/{id}`, `DELETE /borrow-records/{id}` |
| **Saúde** | `GET /health_check` |

---

## Próximos Passos

- [Modelos de Dados (ERD)](data-models-erd.md)
