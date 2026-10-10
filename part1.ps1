# Part 1: Root Configuration Files
# Run this script in the project root directory

Write-Host "Creating Part 1: Root Configuration Files..." -ForegroundColor Green

# Function to write file content
function Write-FileContent {
    param(
        [string]$Path,
        [string]$Content
    )
    
    $directory = Split-Path -Parent $Path
    if (-not (Test-Path $directory)) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }
    
    Set-Content -Path $Path -Value $Content -Force
    Write-Host "Created: $Path" -ForegroundColor Cyan
}

# ============================================
# FILE 1: .gitignore
# ============================================
$gitignoreContent = '# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment Variables
.env
.env.local
.env.*.local

# Data
data/raw/
data/bronze/
data/silver/
data/gold/
data/quarantine/
data/incoming/*.csv
data/incoming/*.json

# Airflow
airflow/logs/
airflow/*.db
airflow/webserver_config.py

# Spark
spark-warehouse/
metastore_db/

# PostgreSQL
*.sql.backup

# Logs
*.log
logs/

# Jupyter Notebooks
.ipynb_checkpoints/
*.ipynb

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# MyPy
.mypy_cache/
.dmypy.json
dmypy.json

# Certificates
*.pem
*.key
*.crt

# Temporary files
tmp/
temp/
*.tmp

# OS
Thumbs.db
.DS_Store'
Write-FileContent -Path ".gitignore" -Content $gitignoreContent

# ============================================
# FILE 2: README.md
# ============================================
$readmeContent = '# RetailPulse - End-to-End Retail Data Engineering Platform

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
```bash
git clone https://github.com/BapunReact01/retailpulse-data-platform.git
cd retailpulse-data-platform