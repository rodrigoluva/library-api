# Testes

A Library API utiliza o **pytest** para garantir a correção da aplicação por meio de testes automatizados. O conjunto de testes abrange autenticação, autorização, comportamento dos endpoints, validação de requisições e interações com o banco de dados.

## Stack de Testes

O projeto utiliza as seguintes ferramentas:

* **pytest** – Executor de testes.
* **pytest-asyncio** – Suporte para testes assíncronos.
* **FastAPI TestClient** – Cliente HTTP para testes de endpoints.
* **SQLite In-Memory Database** – Banco de dados em memória isolado, criado para cada sessão de testes.
* **SQLAlchemy Async** – Operações assíncronas com banco de dados.

## Executando os testes

Execute a suíte de testes completa:

```bash
poetry run task test
```

## Banco de Dados de Testes

Os testes utilizam um **banco de dados SQLite em memória**, o que proporciona:

* Execução rápida.
* Isolamento entre as execuções dos testes.
* Ausência de modificações no banco de dados de desenvolvimento.
* Criação e limpeza automáticas do banco de dados.

Cada teste começa com um banco de dados limpo, garantindo que os testes permaneçam independentes e reproduzíveis.

## Estrutura de Testes

```
tests/
├── conftest.py
├── test_auth.py
├── test_authors.py
├── test_book_copies.py
├── test_books.py
├── test_borrow_records.py
├── test_db.py
├── test_health_check.py
└── test_users.py
```

### `conftest.py`

As *fixtures* compartilhadas são definidas no arquivo `conftest.py`, incluindo:

* Sessão de banco de dados
* Cliente de teste
* Tokens de autenticação
* Usuários de exemplo
* Autores
* Livros
* Exemplares de livros
* Registros de empréstimo

O uso de *fixtures* reduz a duplicação de código e mantém os testes concisos.

## Estratégia de Testes

Cada *endpoint* é testado quanto aos seus comportamentos principais, incluindo:

* Requisições bem-sucedidas
* Autenticação (`401 Unauthorized`)
* Autorização (`403 Forbidden`)
* Recurso não encontrado (`404 Not Found`)
* Erros de validação (`422 Unprocessable Entity`)
* Violações de regras de negócio (`400 Bad Request` / `409 Conflict`)

Sempre que aplicável, os testes também verificam se o estado do banco de dados é alterado corretamente após uma operação.

## Exemplo de Teste

```python
def test_get_user_success(client, admin_token, user):
response = client.get(
f"/api/v1/users/{user.id}",
headers={"Authorization": f"Bearer {admin_token}"},
)

assert response.status_code == 200

data = response.json()

assert data["id"] == user.id
assert data["email"] == user.email
```

## Fixtures

Fixtures fornecem dados de teste e dependências reutilizáveis.

Exemplos incluem:

* `client`
* `session`
* `admin_token`
* `librarian_token`
* `member_token`
* `user`
* `author`
* `book`
* `book_copy`
* `borrowed_record`

O uso de fixtures mantém os testes focados no comportamento esperado, em vez da lógica de configuração.

## Melhores Práticas

* Mantenha os testes independentes.
* Crie apenas os dados necessários para cada teste.
* Prefira o uso de *fixtures* em vez de código de configuração duplicado.
* Verifique tanto a resposta HTTP quanto as alterações no banco de dados.
* Escreva nomes de testes descritivos que expressem claramente o comportamento esperado.
* Teste tanto os fluxos de sucesso quanto os cenários de falha.

## Testes Contínuos

Antes de abrir um *pull request* ou realizar o *merge* de alterações, execute a suíte de testes completa para garantir que as novas alterações não introduzam regressões.

Uma suíte de testes aprovada ajuda a manter a confiabilidade e a estabilidade da Library API à medida que o projeto evolui.
