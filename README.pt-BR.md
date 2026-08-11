# Library API

## Visão Geral

A Library API é uma API RESTful para o gerenciamento de um sistema de biblioteca. Ela disponibiliza endpoints para gerenciar usuários, autores, livros, exemplares e registros de empréstimo, possibilitando uma gestão eficiente do catálogo e fluxos de trabalho de empréstimo de livros.

A API suporta todo o ciclo de vida dos recursos da biblioteca, incluindo o cadastro de usuários e autores, a manutenção do catálogo de livros, o rastreamento de exemplares físicos individuais e o registro de operações de empréstimo e devolução. Ela foi projetada com uma arquitetura clara e modular, seguindo as melhores práticas de REST.

## Principais Recursos

- **Autenticação e Autorização**: Autenticação baseada em JWT com controle de acesso por funções (Administrador, Bibliotecário, Membro).
- **Gerenciamento de Usuários**: Cadastro, gestão de perfil e atribuição de funções.
- **Gerenciamento de Autores**: Operações CRUD para autores, incluindo dados biográficos.
- **Gerenciamento de Livros**: Ciclo de vida completo do livro, com validação de ISBN e associação com autores.
- **Gerenciamento de Exemplares**: Rastreamento de exemplares físicos com status de disponibilidade.
- **Sistema de Empréstimos**: Registro de saída e devolução com prazos e prevenção de conflitos.
- **Registros de Empréstimos**: Histórico completo de empréstimos com recursos de filtragem.

## Stack Tecnológico

- **Python**: 3.13+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (Async)
- **Validação**: Pydantic V2
- **Banco de dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Migrações**: Alembic
- **Autenticação**: JWT (PyJWT) + Argon2 (pwdlib)
- **CLI**: Typer
- **Docs**: MkDocs + OpenAPI 3.1
- **Linting**: Ruff

## Início Rápido

```bash
# Clone e entre no projeto
cd library-api

# Instale as dependências (usando Poetry)
poetry install

# Configure o ambiente
cp .env.example .env
# Edite o arquivo .env com suas variáveis ​​DATABASE_URL e JWT_SECRET_KEY

# Execute as migrações
poetry run alembic upgrade head

# Crie o usuário administrador
poetry run python -m library_api.cli create-admin-user

# Inicie o servidor de desenvolvimento
poetry run task run
# ou: poetry run fastapi dev library_api/app.py
```
> Se você não tiver o Poetry ou o Git instalados, consulte o guia de [Pré-requisitos](docs/pt-BR/prerequisites.md).

Acesse `http://localhost:8000/docs` para ver a documentação interativa da API (Swagger UI). Caso tenha dúvidas, consulte a documentação na pasta `docs/`.

## Docker Compose

Se você tiver o **Docker** instalado, começar é muito mais simples. Após clonar o repositório e criar o arquivo `.env`, execute o comando abaixo para iniciar a aplicação **Library API** e o banco de dados **PostgreSQL**, aplicar as migrações do banco de dados e disponibilizar a documentação da API.

> [!warning]
> Ao usar o **Docker**, não coloque os valores do arquivo `.env` entre aspas. O Docker lê variáveis ​​de ambiente como strings simples, e a inclusão de aspas pode causar comportamentos inesperados.

```sh
docker compose up
```

Agora, entre no container utilizando:

```sh
docker exec -it libraryapi-app-1 sh
```

Em seguida, execute o comando descrito em [Criar Usuário Administrador Inicial](docs/pt-BR/installation.md#criar-usuário-administrador-inicial) para criar a conta de administrador.

Ao executar a aplicação com o Docker Compose, a documentação da API fica disponível na porta **80**. Abra o seu navegador e acesse `http://localhost` ou `http://127.0.0.1` para visualizá-la.

## Kubernetes

For informations about local deploy using **Kubernetes** go to [Deployment](docs/pt-BR/deployment.md#implantação).

---

## Links Rápidos

- **Documentação da API (Swagger UI)**: `http://localhost:8000/docs`
- **Documentação da API (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`
- **Verificação de Saúde (Health Check)**: `http://localhost:8000/health_check`
- **Site MkDocs**: `poetry run task docs` → `http://localhost:8001`

---

## Licença

Este projeto está licenciado sob os termos da licença MIT.