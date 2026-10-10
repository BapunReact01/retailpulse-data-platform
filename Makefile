Set-Content -Path "Makefile" -Value '.PHONY: help setup build up down restart logs clean test lint format

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@awk "BEGIN {FS = \":.*?## \"} /^[a-zA-Z_-]+:.*?## / {printf \"  %-20s %s\n\", $$1, $$2}" $(MAKEFILE_LIST)

setup:
	@echo "Setting up RetailPulse..."
	@cp .env.example .env
	@echo "Please edit .env with your configuration"
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt

build:
	@docker compose build

up:
	@docker compose up -d

down:
	@docker compose down

restart:
	@docker compose restart

logs:
	@docker compose logs -f

logs-airflow:
	@docker compose logs -f airflow-webserver airflow-scheduler airflow-worker

logs-spark:
	@docker compose logs -f spark-master spark-worker

clean:
	@docker compose down -v
	@docker system prune -f

test:
	@pytest tests/unit/

test-integration:
	@pytest tests/integration/

test-all:
	@pytest tests/

lint:
	@flake8 airflow/ pyspark/ ingestion/ data_quality/
	@mypy airflow/ pyspark/ ingestion/ data_quality/

format:
	@black airflow/ pyspark/ ingestion/ data_quality/
	@isort airflow/ pyspark/ ingestion/ data_quality/

check: lint test

init-db:
	@docker exec -i retailpulse-postgres-ops psql -U retail_user -d retail_ops < warehouse/ddl/01_create_operational_db.sql
	@docker exec -i retailpulse-postgres-dw psql -U retail_user -d retail_dw < warehouse/ddl/02_create_dw_db.sql'