# Stage 1: Build stage
FROM python:3.10 AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1 \
    POETRY_VERSION=1.4.2 \
    POETRY_VIRTUALENVS_CREATE="false"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /build

# Copy the dependency files to leverage caching
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-dev

# Stage 2: Runtime stage
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

WORKDIR /ecommerce_backend

# Copy only necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /build /ecommerce_backend
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

COPY docker-entrypoint.sh ./

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
