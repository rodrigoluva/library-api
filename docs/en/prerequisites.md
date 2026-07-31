# Prerequisites

Before setting up the Library API project, ensure your system meets the following requirements.

## System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: Version 3.13 or higher
- **Poetry**: Python dependency manager (version 1.0 or higher)
- **Git**: For cloning the repository (optional, if you intend to clone the source code)

---

## Software Dependencies

### Python 3.13+

The project uses specific features of Python 3.13+, so having this version installed is essential. You can check your Python version with the command:

```bash
python --version
```

ou

```bash
python3 --version
```

### Poetry

Poetry is used to manage project dependencies. To install Poetry, check the [Poetry Docs](https://python-poetry.org/docs/) or use the following command:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After installation, add the Poetry directory to your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Git

To clone the repository, you will need Git installed:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install git

# CentOS/RHEL/Fedora
sudo dnf install git

# macOS (com Homebrew)
brew install git

# Windows
# Download and install the Git for Windows
```

## Technical Skills

Although not software requirements, the following knowledge is useful in working with this project:

- Experience with Python
- Basic knowledge of REST APIs
- Familiarity with SQL databases
- Basic knowledge of Docker (optional)
- Knowledge of command-line tools

## Optional Tools

- **Docker and Docker Compose**: For running in containers
- **Postman or Insomnia**: For testing API endpoints
- **Text editor or IDE**: Such as VS Code, PyCharm, Vim, etc.


## Next Steps

→ [Installation Guide](installation.md)
