FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application
COPY . .

# Install spacy model
RUN python -m spacy download en_core_web_sm

# Run migrations
RUN alembic upgrade head

EXPOSE 8000

CMD ["uvicorn", "project_tasker.main:app", "--host", "0.0.0.0", "--port", "8000"]
