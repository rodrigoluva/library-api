# Instalação

Este guia orientará você durante a instalação e a configuração inicial da Library API.

## Clonar o Repositório

Primeiro, clone o repositório em sua máquina local:

```bash
git clone <REPOSITORY_URL>
cd library-api
```

Se você já tiver o código-fonte localmente, navegue até o diretório do projeto:

```bash
cd /caminho/para/library-api
```

## Instalando Dependências

O projeto utiliza o Poetry para o gerenciamento de dependências. Instale todas as dependências com o comando:

```bash
poetry install
```

Caso queira instalar apenas as dependências principais (excluindo as de desenvolvimento):

```bash
poetry install --no-dev
```

## Ativando o Ambiente Virtual

Para trabalhar com o ambiente virtual criado pelo Poetry:

```bash
poetry shell
```

Alternativamente, você pode executar comandos dentro do ambiente virtual sem ativá-lo:

```bash
poetry run python script.py
```

## Configuração do Ambiente

### 1. Copiar o Arquivo de Exemplo de Ambiente

```bash
cp .env.example .env
```

### 2. Configurar o Arquivo `.env`

Edite o arquivo `.env` com suas configurações:

```env
# Configuração do Banco de Dados
# Desenvolvimento (SQLite - nenhuma configuração adicional necessária)
DATABASE_URL=sqlite+aiosqlite:///./library.db

# Produção (PostgreSQL com asyncpg)
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/library_api

# Autenticação JWT
JWT_SECRET_KEY=sua-chave-super-secreta-altere-em-producao-min-32-caracteres
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=5
```

### 3. Gerar um Segredo JWT Seguro

```bash
# Usando OpenSSL
openssl rand -base64 32
```

Para mais informações sobre a configuração do projeto, consulte o guia [Configuração do Projeto](configuration.md).

## Configuração do Banco de Dados

### Desenvolvimento (SQLite)

O projeto utiliza o SQLite como banco de dados padrão. Para inicializar o banco de dados, execute as migrações do Alembic:

```bash
# Executar migrações - cria o arquivo library.db automaticamente
poetry run alembic upgrade head
```

Isso criará as tabelas necessárias no banco de dados.

### Produção (PostgreSQL)

```bash
# 1. Criar banco de dados e usuário
sudo -u postgres psql -c "CREATE DATABASE library_api;"
sudo -u postgres psql -c "CREATE USER library_user WITH ENCRYPTED PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE library_api TO library_user;"

# 2. Atualizar o .env com a URL do PostgreSQL
# DATABASE_URL=postgresql+asyncpg://library_user:secure_password@localhost:5432/library_api

# 3. Executar migrações
poetry run alembic upgrade head
```

### Verificar Banco de Dados

```bash
# Verifique o status da migração
poetry run alembic current

# Ver histórico de migração
poetry run alembic history
```

## Criar Usuário Administrador Inicial

A CLI fornece comandos para criar usuários administradores e bibliotecários:

```bash
# Criar usuário administrador (prompts interativos)
poetry run python -m library_api.cli create-admin-user

# Criar usuário bibliotecário (prompts interativos)
poetry run python -m library_api.cli create-librarian-user
```

**Exemplo de interação:**
```
$ poetry run python -m library_api.cli create-admin-user
Name: Admin User
Email: admin@library.com
Password: ********
Password (repeat): ********
Created admin user admin@library.com with id 1
```

## Iniciar o Servidor de Desenvolvimento

```bash
# Usando o Taskipy (definido no pyproject.toml)
poetry run task run

# Ou diretamente com a CLI do FastAPI
poetry run fastapi dev library_api/app.py

# Ou diretamente com o uvicorn
poetry run uvicorn library_api.app:app --reload --host 0.0.0.0 --port 8000
```

### Saída do Servidor

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

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

Em seguida, execute o comando descrito em [Criar Usuário Administrador Inicial](#criar-usuário-administrador-inicial) para criar a conta de administrador.

Ao executar a aplicação com o Docker Compose, a documentação da API fica disponível na porta **80**. Abra o seu navegador e acesse `http://localhost` ou `http://127.0.0.1` para visualizá-la.

## Verificar a Instalação

### Documentação da API

Abra no navegador:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Testar a Autenticação

Se você estiver usando o Swagger UI e já tiver criado um usuário administrador, navegue até o endpoint **Create Access Token**.

- Clique em **Try it out**.
- Insira o e-mail e a senha do usuário administrador que você criou.
- Clique em **Execute**.

Se a solicitação for bem-sucedida, a resposta incluirá um token de acesso. Copie o token e, em seguida, clique em **Authorize** na parte superior da página. Cole o token no campo **Value** e clique em **Authorize** novamente.

Agora você está autenticado e pode acessar todos os endpoints protegidos.

## Iniciar o site de documentação

```bash
# Compilar e servir o site MkDocs
poetry run task docs

# Ou diretamente
poetry run mkdocs serve -a 127.0.0.1:8001
```

Abra http://localhost:8001 no navegador.

## Solução de problemas

### Erro de Versão do Python

Certifique-se de estar usando o Python 3.13 ou superior:

```bash
python --version
```

Se você estiver usando uma versão diferente, pode especificar a versão para o Poetry:

```bash
poetry env use python3.13
poetry install
```

### Falha na Instalação de Dependências

Se ocorrerem erros durante a instalação de dependências, tente limpar o cache do Poetry:

```bash
poetry cache clear pypi --all
poetry install
```

### Reiniciar Banco de Dados (Desenvolvimento)

```bash
# Remover banco de dados SQLite
rm library.db

# Executar novamente as migrações
poetry run alembic upgrade head

# Recriar usuário administrador
poetry run python -m library_api.cli create-admin-user
```

---

## Próximos passos

Agora que a instalação foi concluída, você pode:

- Configurar as variáveis ​​de ambiente necessárias ([Configuração do Projeto](configuration.md))
- Explorar os endpoints da API ([Endpoints da API](api-endpoints.md))
