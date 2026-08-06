FROM python:3.13.11-alpine3.23

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

ARG USERNAME=libaryapi
ENV POETRY_VERSION=2.3.1 \
    PATH="/home/${USERNAME}/.local/bin:$PATH"

RUN apk add curl=8.20.0-r0 \
      --no-cache && \
    rm -rf /var/cache/apk/* && \
    adduser -s /bin/sh -D ${USERNAME}

USER ${USERNAME}

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /home/${USERNAME}

COPY --chown=${USERNAME}:${USERNAME} pyproject.toml poetry.lock ./
RUN poetry install \
      --without dev \
      --no-root \
      --no-ansi

COPY --chown=${USERNAME}:${USERNAME} . .

CMD ["poetry", "run", "fastapi", "dev", "library_api/app.py", "--host", "0.0.0.0"]
