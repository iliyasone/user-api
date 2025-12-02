FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    bash ca-certificates tzdata

WORKDIR /app
RUN touch README.md
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

RUN uv sync --locked

COPY . .

RUN find . -name "__pycache__" -type d -exec rm -rf {} + \
    && rm -f config/local.py || true

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
