Set-Content -Path "README.md" -Value '# RetailPulse - End-to-End Retail Data Engineering Platform

A production-style end-to-end data engineering platform that demonstrates modern data pipeline architecture using Apache Airflow, PySpark, PostgreSQL, and Docker.

## Project Overview

RetailPulse is a comprehensive data platform that ingests data from multiple sources (REST APIs, CSV files, PostgreSQL), processes it using PySpark in a Medallion architecture (Bronze -> Silver -> Gold), validates data quality, and loads it into a Star Schema data warehouse for analytics.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | Apache Airflow 2.8.0 |
| Processing | PySpark 3.5.0 |
| Database | PostgreSQL 15 |
| Storage | Parquet |
| API | Python + Flask (Mock) |
| Containerization | Docker & Docker Compose |
| Testing | Pytest |
| CI/CD | GitHub Actions |

## Quick Start

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Git
- 8GB+ RAM available for Docker

### Setup

1. Clone the repository:
git clone https://github.com/BapunReact01/retailpulse-data-platform.git
cd retailpulse-data-platform

2. Copy environment variables:
cp .env.example .env

3. Start all services:
docker compose up -d

4. Access services:
- Airflow Web UI: http://localhost:8080
- Spark Master UI: http://localhost:8081
- PgAdmin: http://localhost:5050
- Mock API: http://localhost:5000

## Data Pipeline

The pipeline consists of 4 main DAGs:

1. retail_ingestion_dag: Ingests data from API, CSV, and PostgreSQL
2. retail_transformation_dag: Runs PySpark transformations (Bronze -> Silver -> Gold)
3. retail_warehouse_dag: Loads data into Star Schema warehouse
4. data_quality_dag: Runs data quality checks and generates reports

## License

MIT License - see LICENSE file for details'