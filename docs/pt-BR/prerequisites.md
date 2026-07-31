# Pré-requisitos

Antes de configurar o projeto da API da biblioteca, certifique-se de que seu sistema atenda aos seguintes requisitos.

## Requisitos do Sistema

- **Sistema Operacional**: Linux, macOS ou Windows
- **Python**: Versão 3.13 ou superior
- **Poetry**: Gerenciador de dependências do Python
- **Git**: Para clonar o repositório (opcional, caso pretenda clonar o código-fonte)

---

## Software Dependencies

### Python 3.13+

O projeto utiliza recursos específicos do Python 3.13+, então é essencial ter essa versão instalada. Você pode verificar sua versão do Python com o comando:

```bash
python --version
```

ou

```bash
python3 --version
```

### Poetry

O Poetry é utilizado para gerenciar dependências de projetos. Para instalar o Poetry, consulte a [documentação do Poetry](https://python-poetry.org/docs/) ou utilize o seguinte comando:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Após a instalação, adicione o diretório do Poetry ao seu PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Git

Para clonar o repositório, você precisará do Git instalado:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install git

# CentOS/RHEL/Fedora
sudo dnf install git

# macOS (com Homebrew)
brew install git

# Windows
# Baixe e instale o Git for Windows
```

## Habilidades Técnicas

Embora não sejam requisitos de software, os seguintes conhecimentos são úteis para trabalhar neste projeto:

- Experiência com Python
- Conhecimento básico de APIs REST
- Familiaridade com bancos de dados SQL
- Conhecimento básico de Docker (opcional)
- Conhecimento de ferramentas de linha de comando

## Ferramentas Opcionais

- **Docker e Docker Compose**: Para execução em containers
- **Postman ou Insomnia**: Para testar endpoints da API
- **Editor de texto ou IDE**: Como VS Code, PyCharm, Vim, etc.


## Próximos passos

Com esses pré-requisitos atendidos, você estará pronto para prosseguir com a [instalação](installation.md) do projeto.
