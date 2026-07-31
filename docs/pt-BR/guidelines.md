# Diretrizes e Padrões

Estilo de código, padrões de arquitetura e melhores práticas para o projeto da Library API.

---

## Estilo de Código Python

### Formatação e Linting (Ruff)

```bash
# Verificar estilo
poetry run task lint

# Correção automática
poetry run task pre_format

# Apenas formatar
poetry run task format
```

**Configuração do Ruff** (`pyproject.toml`):
```toml
[tool.ruff]
line-length = 79
preview = true

[tool.ruff.lint]
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
ignore = ['PLR2004', 'PLR0917', 'PLR0913']

[tool.ruff.format]
preview = true
quote-style = 'single'
```

### Principais Regras de Estilo

- **Comprimento da linha:** Máximo de 79 caracteres.
- **Aspas:** Use aspas simples (`'`).
- **Imports:** Mantenha os imports ordenados utilizando o isort (regra `I` do Ruff).
- **Type hints:** Obrigatórios para todas as funções públicas.
- **Async:** Use `async def` para todas as funções de I/O.

---

## Padrões de Arquitetura

### Estrutura de Camadas

```
library_api/
├── app.py                 # Fábrica da aplicação FastAPI
├── cli.py                 # Comandos da CLI com Typer
├── core/                  # Preocupações transversais
│   ├── database.py        # Engine e sessão assíncronas
│   ├── security.py        # Autenticação, JWT, hashing de senha
│   └── settings.py        # Configurações com Pydantic
├── dependencies/          # Dependências do FastAPI
│   └── permissions.py     # Controle de acesso baseado em funções (RBAC)
├── models/                # Modelos ORM do SQLAlchemy
│   ├── base.py            # DeclarativeBase
│   ├── users.py           # Modelo de usuário + enum de função (Role)
│   └── books.py           # Author, Book, BookCopy, BorrowRecord
├── routers/               # Endpoints da API (controllers)
│   ├── auth.py            # /token, /refresh_token
│   ├── users.py           # /users/*
│   ├── authors.py         # /authors/*
│   ├── books.py           # /books/*
│   ├── book_copies.py     # /book-copies/*, /books/{id}/copies
│   └── borrow_records.py  # /borrow-records/*, /books/{id}/borrow|return
└── schemas/               # Modelos Pydantic v2 (contratos da API)
├── auth.py
├── users.py
├── authors.py
├── books.py
├── book_copies.py
└── borrow_records.py
```

---
## Convenções de Nomenclatura


- **Pacotes/Módulos:** use `snake_case`. 
    - Exemplo: `book_copies.py`.
- **Classes:** use `PascalCase`. 
    - Exemplos: `BookCopy`, `UserRole`.
- **Funções/Métodos:** use `snake_case`. 
    - Exemplo: `create_book_copy()`.
- **Variáveis:** use `snake_case`. 
    - Exemplo: `book_copy_id`.
- **Constantes:** use `UPPER_SNAKE_CASE`. 
    - Exemplo: `JWT_EXPIRATION_MINUTES`.
- **Enums:** use `PascalCase` para classes de enumeração e acesse os membros como `EnumClass.MEMBER`. 
    - Exemplo: `UserRole.ADMIN`.
- **Tabelas de Banco de Dados:** use `snake_case` no plural. 
    - Exemplo: `book_copies`.
- **Colunas de Banco de Dados:** use `snake_case`. 
    - Exemplo: `created_at`.
- **Caminhos de API:** use `kebab-case` no plural. 
    - Exemplo: `/book-copies`.
- **Parâmetros de Consulta (Query Params):** use `snake_case`. 
    - Exemplo: `book_copy_id`.
- **Classes de Schema:** use `PascalCase` com sufixo descritivo. 
    - Exemplos: `BookCopyCreateSchema`, `BookCopyPublicSchema`.

### Padrão de Nomenclatura de Schemas

```
{Entidade}{Operação}Schema
│
├── CreateSchema     # Corpo da requisição POST
├── UpdateSchema     # Corpo da requisição PUT/PATCH (todos opcionais)
├── PublicSchema     # Resposta com objeto único
├── ListPublicSchema # Resposta com lista paginada
└── Relationship...  # Relacionamentos aninhados
```

---

## Diretrizes de Segurança

### Autenticação

- **Nunca registre (log) senhas ou tokens**
- **Use `pwdlib` com Argon2** para hashing de senhas (já configurado)
- **Tokens JWT**: Expiração curta (5-15 min), segredo seguro
- **Apenas HTTPS** em produção
- **Valide todas as entradas** com esquemas Pydantic

### Autorização

- **Acesso baseado em funções** via dependência `require_roles()`
- **Permissões explícitas** por endpoint
- **Restrito a administradores** para operações destrutivas (DELETE)
- **Acesso de membros** limitado aos próprios dados (emprestar/devolver os próprios livros)

### Proteção de Dados

- **Nunca exponha hashes de senha** nas respostas
- **Use esquemas separados** para entrada e saída
- **Higienize as mensagens de erro** (sem *stack traces* em produção)
- **Limitação de taxa** (*rate limiting*) (recomendado para produção)

---

## Diretrizes de Banco de Dados

### Migrações (Alembic)

```bash
# Criar migração
poetry run alembic revision --autogenerate -m "descrição"

# Aplicar migrações
poetry run alembic upgrade head

# Reverter (rollback)
poetry run alembic downgrade -1
```

### Nomenclatura de Migrações

```
{revisão}_{descrição}.py
# Exemplos:
b9e0f87139b3_create_users_table.py
d58754e7c566_create_authors_books_book_copies_and_borrow_records.py
2f8a67030948_feat_add_users_role.py
```

### Diretrizes de Modelos

- **Herde de `Base`** (`library_api.models.base.Base`)
- **Use `Mapped` + `mapped_column`** (estilo SQLAlchemy 2.0)
- **Defina relacionamentos** com `relationship()` e `back_populates`
- **Use `TYPE_CHECKING`** para referências antecipadas (*forward references*)
- **Adicione `created_at` / `updated_at`** a todas as tabelas
- **Use enums** para colunas de valores fixos (`UserRole`, `BookStatus`)

---

## Diretrizes de Design de API

### Convenções REST

| Operação | Método | Caminho | Status | Corpo |
|-----------|--------|------|--------|------|
| Listar | GET | `/resource` | 200 | - |
| Criar | POST | `/resource` | 201 | CreateSchema |
| Obter um | GET | `/resource/{id}` | 200 | - |
| Atualizar | PUT | `/resource/{id}` | 200 | UpdateSchema |
| Excluir | DELETE | `/resource/{id}` | 204 | - |
| Ação personalizada | POST | `/resource/{id}/action` | 200/201 | Schema |

### Padrões de Resposta

```python
# Objeto único
return db_object  # Serializado automaticamente via response_model

# Lista paginada
return {
"items": objects,
"offset": offset,
"limit": limit,
}

# Resposta de ação personalizada
return {"copies": created_copies, "quantity": quantity}
```

### Respostas de Erro

| Status | Quando | Formato |
|--------|------|--------|
| 400 | Violação de regra de negócio | `{"detail": "isbn already in use"}` |
| 401 | Token ausente/inválido | `{"detail": "Not authenticated"}` |
| 403 | Permissões insuficientes | `{"detail": "not enough permissions"}` |
| 404 | Recurso não encontrado | `{"detail": "book not found"}` |
| 409 | Conflito (ex.: já emprestado) | `{"detail": "no available copies"}` |
| 422 | Erro de validação | Formato de erro do Pydantic |

---

## Diretrizes de Teste

### Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py          # Fixtures do Pytest
├── test_auth.py         # Testes de autenticação
├── test_users.py        # Testes de CRUD de usuários
├── test_authors.py      # Testes de CRUD de autores
├── test_books.py        # Testes de CRUD de livros
├── test_book_copies.py  # Testes de CRUD de exemplares
└── test_borrow_records.py # Testes do fluxo de empréstimo
```

---

## Gerenciamento de Dependências

### Adicionando Dependências

```bash
# Dependência de produção
poetry add package-name

# Dependência de desenvolvimento
poetry add --group dev package-name

# Grupo de dependência opcional
poetry add --group optional package-name
```

### Fixação de Versão

```toml
# pyproject.toml
dependencies = [
"fastapi[standard] (>=0.139.0,<0.140.0)",  # O limite superior evita alterações que quebram a compatibilidade (breaking changes)
]
```

---

## Padrões de Documentação

### Anotações OpenAPI

```python
@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=BookPublicSchema,
    summary='Create Book - [ADMIN, LIBRARIAN]',
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'content': {
                'application/json': {
                    'example': {'detail': 'isbn already in use'}
                }
            }
        },
    },
)
```

---

## Fluxo de Trabalho do Git

### Nomenclatura de Branches

| Tipo | Padrão | Exemplo |
|------|---------|---------|
| Feature | `feat/{descrição-curta}` | `feat/add-borrow-records-crud` |
| Fix | `fix/{descrição-curta}` | `fix/token-refresh-expiry` |
| Docs | `docs/{descrição-curta}` | `docs/add-mkdocs` |
| Chore | `chore/{descrição-curta}` | `chore/add-ruff-taskipy` |
| Refactor | `refactor/{descrição-curta}` | `refactor/security-module` |

### Mensagens de Commit

Siga o padrão Conventional Commits:

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

| Tipo | Descrição |
|------|-------------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Apenas documentação |
| `style` | Formatação, sem alteração na lógica |
| `refactor` | Reestruturação de código |
| `chore` | Manutenção, dependências, build |
| `test` | Adição de testes |

**Exemplos:**
```
feat(auth): adicionar endpoint de refresh token
fix(books): impedir ISBN duplicado na atualização
docs: adicionar configuração do mkdocs
chore: adicionar ruff e taskipy como dependências de desenvolvimento
```

---

## Next Steps

- [Project Structure](project-structure.md)
