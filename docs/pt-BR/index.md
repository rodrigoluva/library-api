# Documentação da Library API

## Visão Geral do Projeto

A **Library API** é uma API RESTful moderna e assíncrona construída com **FastAPI** para gerenciar um sistema de biblioteca. Ela oferece funcionalidades completas para gerenciar usuários, autores, livros, cópias de livros e registros de empréstimos com controle de acesso baseado em funções (RBAC).

### Principais Recursos

- **Autenticação e Autorização**: Autenticação baseada em JWT com controle de acesso por funções (Administrador, Bibliotecário, Membro).
- **Gerenciamento de Usuários**: Cadastro, gestão de perfil e atribuição de funções.
- **Gerenciamento de Autores**: Operações CRUD para autores, incluindo dados biográficos.
- **Gerenciamento de Livros**: Ciclo de vida completo do livro, com validação de ISBN e associação com autores.
- **Gerenciamento de Exemplares**: Rastreamento de exemplares físicos com status de disponibilidade.
- **Sistema de Empréstimos**: Registro de saída e devolução com prazos e prevenção de conflitos.
- **Registros de Empréstimos**: Histórico completo de empréstimos com recursos de filtragem.

### Stack Tecnológico

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

### Destaques da Arquitetura

- Design **orientado a assincronia** (*async-first*) com uso de `async/await` em toda a aplicação
- Separação baseada em **arquitetura limpa** (*Clean Architecture*): roteadores → esquemas → modelos → núcleo (*core*)
- **Injeção de dependência** para sessões de banco de dados e autenticação
- **Permissões baseadas em funções** (*role-based*) via dependências do FastAPI
- **Migrações de banco de dados** com Alembic (suporte a assincronia)
- Especificação **OpenAPI 3.1** gerada automaticamente
- **Segurança de tipos** com validação completa via Pydantic v2

---

## Primeiros passos

Para começar a usar esta API, siga as etapas descritas na seção [Instalação](installation.md). A API está pronta para ser integrada a aplicações front-end ou utilizada diretamente por meio de requisições HTTP.

### Documentação

- [Pré-requisitos](prerequisites.md)
- [Instalação](installation.md)
- [Configuração](configuration.md)
- [Diretrizes e Padrões](guidelines.md)
- [Estrutura do Projeto](project-structure.md)
- [Endpoints da API](api-endpoints.md)
- [Modelos de Dados (ERD)](data-models-erd.md)
- [Arquitetura do Sistema](system-architecture.md)
- [Deploy](deployment.md)

---

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](../LICENSE) para detalhes.

---

## Autor

**Rodrigo Valladão** - [rodrigoluva@gmail.com](mailto:rodrigoluva@gmail.com)

---

*Última atualização: Julho 2025*
