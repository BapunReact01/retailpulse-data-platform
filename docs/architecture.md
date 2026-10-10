# RetailPulse System Architecture

## Overview

RetailPulse is a modern data engineering platform designed to ingest, process, and analyze retail data from multiple sources. The architecture follows industry best practices with clear separation of concerns across layers.

## High-Level Architecture
┌─────────────────────────────────────────────────────────────────┐
│ EXTERNAL SOURCES │
├──────────────────┬──────────────────┬──────────────────────────┤
│ REST API │ CSV Files │ Operational DB │
│ (Mock API) │ (Daily dumps) │ (PostgreSQL) │
└────────┬─────────┴────────┬─────────┴──────────┬───────────────┘
│ │ │
▼ ▼ ▼
┌─────────────────────────────────────────────────────────────────┐
│ INGESTION LAYER │
│ API Ingestor | CSV Ingestor | PostgreSQL Extractor │
└────────────────────────┬────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ ORCHESTRATION LAYER │
│ Apache Airflow │
└────────────────────────┬────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ PROCESSING LAYER │
│ PySpark (Medallion) │
│ Bronze -> Silver -> Gold │
└────────────────────────┬────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ DATA QUALITY LAYER │
│ Schema | Business Rules | Referential | Statistical │
└────────────────────────┬────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ DATA WAREHOUSE LAYER │
│ PostgreSQL (Star Schema) │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ BI & ANALYTICS LAYER │
│ Power BI | SQL Queries │
└─────────────────────────────────────────────────────────────────┘


## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Orchestration | Apache Airflow 2.8.0 | Pipeline orchestration, scheduling, monitoring |
| Processing | PySpark 3.5.0 | Distributed data transformation |
| Database | PostgreSQL 15 | Operational database & Data Warehouse |
| Storage | Parquet | Columnar storage format for Spark |
| API | Python + Flask | Mock REST API for customer/product/store data |
| Containerization | Docker | Reproducible deployment |
| Message Broker | Redis | Celery broker for Airflow |
| Testing | Pytest | Unit and integration testing |
| CI/CD | GitHub Actions | Automated testing and deployment |

## Data Flow

### 1. Ingestion

Data is ingested from three sources:
- REST API: Customer, Product, Store data via HTTP requests
- CSV Files: Daily order dumps from external systems
- PostgreSQL: Transactional data from operational database

All ingested data is stored in the Raw Layer (/data/raw/) in its original format.

### 2. Orchestration

Apache Airflow orchestrates the entire pipeline through 4 DAGs:
- retail_ingestion_dag: Manages data ingestion from all sources
- retail_transformation_dag: Orchestrates PySpark transformations
- retail_warehouse_dag: Loads data into the data warehouse
- data_quality_dag: Runs data quality checks

### 3. Processing (Medallion Architecture)

#### Bronze Layer
- Deduplication
- Basic data type validation
- Null handling
- Schema enforcement
- Audit columns added

#### Silver Layer
- Joins with dimensions (customers, products, stores)
- Business logic application
- Derived field calculations
- Data enrichment

#### Gold Layer
- Final curated datasets
- Query optimization
- Date-based partitioning
- Aggregate metrics

### 4. Data Quality

Comprehensive validation at each stage:
- Schema validation
- Business rules validation
- Referential integrity checks
- Statistical anomaly detection
- Quarantine system for invalid records

### 5. Data Warehouse

Star Schema implementation:
- Fact Table: fact_sales (transactional data)
- Dimension Tables: dim_date, dim_customer, dim_product, dim_store
- SCD Type 2: Historical tracking for dimensions
- Aggregate Tables: Performance optimization