# FROM python:3.12-slim
# WORKDIR /app
# COPY pyproject.toml uv.lock /app/
# RUN pip install --no-cache-dir uv
# COPY app /app/app
# RUN uv sync
# CMD ["/bin/sh", "-c", "uv run uvicorn --reload --reload-dir . --host 0.0.0.0 --port $BACKEND_PORT app.main:app"]

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv (dependency manager)
RUN pip install --no-cache-dir uv

# Copy project files for dependency resolution
COPY pyproject.toml uv.lock /app/

# Install dependencies using uv (creates .venv)
RUN uv sync

# Copy app source code + migrations + start script
COPY app /app/app
# COPY alembic /app/alembic
# COPY alembic.ini prestart.py start-dev.sh /app/
COPY start-dev.sh /app/

# Make start-dev.sh executable
RUN chmod +x /app/start-dev.sh

# Do NOT hardcode the port (Cloud Run injects $PORT)
CMD ["sh", "/app/start-dev.sh"]