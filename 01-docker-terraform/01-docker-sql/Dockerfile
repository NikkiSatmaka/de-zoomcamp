FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=01-docker-terraform/01-docker-sql/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable --no-dev

COPY uv.lock /app
COPY 01-docker-terraform/01-docker-sql/pyproject.toml /app
COPY 01-docker-terraform/01-docker-sql/ingest_data.py /app/ingest_data.py

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable --no-dev

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT [ "python", "ingest_data.py" ]
