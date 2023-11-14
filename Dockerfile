FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1 \
    POETRY_VERSION=1.4.2 \
    POETRY_VIRTUALENVS_CREATE="false"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /ecommerce_backend

# Copy the project files
COPY pyproject.toml poetry.lock docker-entrypoint.sh ./

RUN chmod +x docker-entrypoint.sh

RUN poetry install --no-interaction --no-ansi --no-dev

ENTRYPOINT ["./docker-entrypoint.sh"]
