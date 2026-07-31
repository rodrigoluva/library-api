# Configuração

Referência completa de todas as opções de configuração do projeto Library API.

---

## Variáveis ​​de Ambiente

Toda a configuração é gerenciada por meio de variáveis ​​de ambiente utilizando o **Pydantic Settings**. Crie um arquivo `.env` na raiz do projeto:

```bash
cp .env.example .env
```

---

## Variáveis ​​Obrigatórias

| Variável | Descrição | Exemplo |
|----------|-------------|---------|
| `DATABASE_URL` | String de conexão com o banco de dados (formato assíncrono do SQLAlchemy) | `sqlite+aiosqlite:///./library.db` ou `postgresql+asyncpg://user:pass@localhost/db` |
| `JWT_SECRET_KEY` | Chave secreta para assinar tokens JWT (mín. 32 caracteres) | `your-super-secret-key-change-in-production` |

---

## Variáveis ​​Opcionais

| Variável | Padrão | Descrição | Exemplo |
|----------|---------|-------------|---------|
| `JWT_ALGORITHM` | `HS256` | Algoritmo de assinatura JWT | `HS256`, `RS256` |
| `JWT_EXPIRATION_MINUTES` | `5` | Tempo de vida do token de acesso em minutos | `15`, `30`, `60` |

---

## Exemplo Completo de `.env`

### Desenvolvimento (SQLite)

```env
# Banco de dados
DATABASE_URL=sqlite+aiosqlite:///./library.db

# Autenticação JWT
JWT_SECRET_KEY=dev-secret-key-change-in-production-minimum-32-characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

### Produção (PostgreSQL)

```env
# Banco de dados
DATABASE_URL=postgresql+asyncpg://library_user:secure_password@localhost:5432/library_api

# Autenticação JWT
JWT_SECRET_KEY=super-secure-random-key-at-least-32-chars-generated-by-openssl
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
```

### Docker/Container

```env
# Banco de dados (usando o nome do serviço Docker)
DATABASE_URL=postgresql+asyncpg://library_user:secure_password@postgres:5432/library_api

# Autenticação JWT
JWT_SECRET_KEY=${JWT_SECRET_KEY}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
```

### Gerar Segredos de Produção

```bash
# Segredo JWT
openssl rand -base64 32
```

---

## Formatos de URL de Banco de Dados

| Banco de Dados | Formato | Exemplo |
|----------|--------|---------|
| **SQLite (async)** | `sqlite+aiosqlite:///path/to/db` | `sqlite+aiosqlite:///./library.db` |
| **PostgreSQL (asyncpg)** | `postgresql+asyncpg://user:pass@host:port/db` | `postgresql+asyncpg://user:pass@localhost:5432/library_api` |

> **Nota**: Este projeto utiliza **SQLAlchemy assíncrono**; portanto, o driver do banco de dados deve oferecer suporte a operações assíncronas (aiosqlite, asyncpg).

---

## Configuração de Segurança

### Tokens JWT

A API utiliza autenticação baseada em JWT (JSON Web Token). Por padrão, os tokens são válidos por 5 minutos, conforme definido pela variável `JWT_EXPIRATION_MINUTES`.

### Hashing de Senhas

As senhas são armazenadas utilizando o algoritmo de hashing Argon2, que é resistente a ataques de força bruta.

---

## Detalhes da Configuração do JWT

### Estrutura do Token

```json
{
"sub": "1",           // ID do usuário (subject)
"exp": 1699999999,    // Timestamp de expiração (UTC)
"iat": 1699999999     // Timestamp de emissão (UTC)
}
```

### Opções de Algoritmo

| Algoritmo | Tipo de Chave | Caso de Uso |
|-----------|----------|----------|
| `HS256` | Simétrica (segredo compartilhado) | Implantações simples, serviço único |
| `RS256` | Assimétrica (par de chaves RSA) | Microsserviços, sistemas distribuídos |
| `ES256` | Assimétrica (ECDSA) | Alta segurança, chaves menores |

> **Implementação Atual**: Apenas `HS256` é suportado. Para RS256/ES256, modifique `library_api/core/security.py`.

### Recomendações de Expiração

| Ambiente | Token de Acesso | Token de Atualização |
|-------------|--------------|---------------|
| Desenvolvimento | 30-60 min | 7-30 dias |
| Homologação | 15-30 min | 7 dias |
| Produção | 5-15 min | 1-7 dias |

> **Nota de Segurança**: Tokens de acesso de curta duração (5-15 min) combinados com tokens de atualização oferecem maior segurança. A implementação atual utiliza apenas tokens de acesso.

---

## Referência da Classe Settings

A configuração é carregada em `library_api/core/settings.py`:

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

### Acessando as Configurações

```python
from library_api.core.settings import Settings

settings = Settings()
print(settings.DATABASE_URL)
print(settings.JWT_SECRET_KEY)
```

> **Importante**: `Settings()` é uma classe que se comporta como um *singleton*. Cada instanciação lê o arquivo `.env`. Utilize a instância definida no nível do módulo em `library_api/core/security.py`:
> ```python
> from library_api.core.settings import Settings
> settings = Settings()  # Instância única utilizada em toda a aplicação
> ```

---

## Configuração do Servidor

### FastAPI

A aplicação está configurada em `library_api/app.py` e pode ser iniciada com diferentes opções:

```bash
# Modo de desenvolvimento com recarregamento automático
poetry run fastapi dev library_api/app.py

# Modo de produção
poetry run uvicorn library_api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Parâmetros de Configuração

- `--host`: Endereço IP para escuta (padrão: 127.0.0.1)
- `--port`: Porta para escuta (padrão: 8000)
- `--workers`: Número de workers (padrão: 1; útil apenas em produção)
- `--reload`: Habilita a recarga automática (apenas para desenvolvimento)

---

## Configuração do Alembic (Migrações)

O projeto utiliza o Alembic para o gerenciamento de migrações de banco de dados. O arquivo de configuração está localizado em `alembic.ini`.

Para executar as migrações:

```bash
# Aplicar todas as migrações pendentes
poetry run alembic upgrade head

# Criar uma nova migração
poetry run alembic revision --autogenerate -m "Descrição da migração"

# Reverter a última migração
poetry run alembic downgrade -1
```

---

## Configuração do Linter e do Formatador

O projeto utiliza o Ruff para linting e formatação de código. As configurações estão no arquivo `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79
exclude = [
# Lista de diretórios excluídos
]

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
ignore = ['PLR2004', 'PLR0917', 'PLR0913']

[tool.ruff.format]
preview = true
quote-style = 'single'
```

Para executar o linter e o formatador:

```bash
# Verificar problemas de estilo
poetry run ruff check

# Corrigir problemas automaticamente
poetry run ruff check --fix

# Formatar o código
poetry run ruff format
```

---

## Configuração do MkDocs

A documentação é gerada utilizando o MkDocs Material. As configurações estão no arquivo `mkdocs.yml`.

Para servir a documentação localmente:

```bash
poetry run mkdocs serve -a 127.0.0.1:8001
```

---

## Próximos passos

Agora você pode voltar ao guia de instalação ou explorar os endpoints da API.

- [Instalação](installation.md)
- [Endpoints da API](api-endpoints.md)
