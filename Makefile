.PHONY: help install install-dev test lint format clean docker-build docker-run deploy-gcp deploy-aws

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install all dependencies including dev"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean generated files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make deploy-gcp   - Deploy to Google Cloud Run"
	@echo "  make deploy-aws   - Deploy to AWS Lambda"

install:
	poetry install --only main

install-dev:
	poetry install
	pre-commit install

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage

docker-build:
	docker build -t agentic-ai-app:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

deploy-gcp:
	gcloud run deploy agentic-ai-app \
		--source . \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated

deploy-aws:
	@echo "AWS deployment not yet implemented"

run-local:
	streamlit run app/main.py

run-api:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
