# syntax=docker/dockerfile:1.4
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     curl     && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy dependency files
COPY pyproject.toml poetry.lock* ./
COPY constraints.txt ./

# Install dependencies with constraints
RUN python -m pip install --upgrade pip &&     pip install -r constraints.txt &&     poetry config virtualenvs.create false &&     poetry install --no-dev --no-interaction --no-ansi

# Copy application
COPY . .

# Install spacy model
RUN python -m spacy download en_core_web_sm

# Run security scan
RUN pip install safety bandit &&     safety check &&     bandit -r project_tasker/

FROM python:3.10-slim AS runtime

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app/project_tasker ./project_tasker
COPY --from=builder /app/alembic.ini ./
COPY --from=builder /app/pyproject.toml ./
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Create non-root user
RUN useradd -m -r appuser &&     chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "project_tasker.main:app", "--host", "0.0.0.0", "--port", "8000"]
