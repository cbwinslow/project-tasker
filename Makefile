.PHONY: help install test lint clean docs serve

help:
	@echo "Available commands:"
	@echo "  install    Install project dependencies"
	@echo "  test       Run tests"
	@echo "  lint       Run linters"
	@echo "  clean      Clean up build artifacts"
	@echo "  docs       Generate documentation"
	@echo "  serve      Start development server"

install:
	./setup-dev.sh

test:
	poetry run pytest tests/ --cov=project_tasker --cov-report=term-missing

lint:
	poetry run black .
	poetry run isort .
	poetry run flake8 .
	poetry run mypy .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

docs:
	poetry run sphinx-build -b html docs/source docs/build

serve:
	poetry run uvicorn project_tasker.main:app --reload --host 0.0.0.0 --port 8000
