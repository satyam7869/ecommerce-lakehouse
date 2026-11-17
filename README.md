# End-to-End E-commerce Lakehouse & Data Warehouse Platform

## Project Overview

This project aims to build an end-to-end E-commerce Data Engineering platform using modern cloud and data engineering technologies.

The platform will demonstrate data ingestion, distributed processing, lakehouse architecture, workflow orchestration, cloud data warehousing, SQL-based transformations, and pipeline reliability.

The project uses a seven-table e-commerce dataset containing approximately 14.3 million records.

## Project Objectives

- Build automated data ingestion pipelines.
- Store source data in AWS S3.
- Process large datasets using Apache Spark and PySpark.
- Implement a Bronze, Silver, and Gold Lakehouse architecture using Delta Lake.
- Orchestrate workflows using Apache Airflow.
- Load and manage analytical data in Snowflake.
- Build transformation models using dbt.
- Implement logging, monitoring, validation, and failure handling.
- Apply Git-based version control and CI/CD practices.

## Technology Stack

| Technology | Planned Usage |
|---|---|
| Python | Data ingestion and automation |
| AWS S3 | Cloud data lake storage |
| PySpark | Distributed data processing |
| Databricks | Spark execution environment |
| Delta Lake | Lakehouse storage architecture |
| Apache Airflow | Workflow orchestration |
| Snowflake | Cloud data warehouse |
| dbt | SQL transformations and data testing |
| Git & GitHub | Version control |
| GitHub Actions | CI/CD automation |

## Dataset Information

**Dataset:** FreeEcommerceTwin14M

**Source:** [Hugging Face Dataset Repository](https://huggingface.co/datasets/HariJha/FreeEcommerceTwin14M)

**Owner:** HariJha

**Format:** Parquet and CSV samples

**Total Records:** 14,328,942

**Number of Tables:** 7

The dataset contains:

- Customers
- Products
- Sessions
- Orders
- Order Items
- Returns
- Support Tickets

**Licence:** CC BY-NC 4.0

The source dataset is synthetic and designed with relational consistency and financial reconciliation characteristics.

## Dataset Exploration

Initial exploration was performed using 50-row CSV samples with Python and Pandas.

The exploration included:

- Schema and data-type inspection
- Null-value analysis
- Duplicate checks
- Descriptive statistics
- Date-column inspection and conversion
- Basic business-rule investigation

The exploration results are documented separately in the `exploration/` directory.

These sample-level findings are not presented as full-dataset validation results.

## Architecture

The planned architecture consists of the following stages:

1. Source Dataset — Hugging Face
2. Ingestion — Python
3. Data Lake — AWS S3
4. Distributed Processing — Databricks and PySpark
5. Lakehouse Storage — Delta Lake
6. Workflow Orchestration — Apache Airflow
7. Data Warehouse — Snowflake
8. Transformations — dbt
9. Analytics — Business-ready data models

Airflow will orchestrate the relevant pipeline tasks across these stages.

## Repository Structure

```text
ecommerce-lakehouse/
├── data/
│   └── samples/
├── exploration/
├── src/
│   ├── ingestion/
│   ├── validation/
│   ├── transformations/
│   └── utils/
├── airflow/
│   └── dags/
├── databricks/
│   └── notebooks/
├── snowflake/
│   └── sql/
├── dbt/
├── tests/
├── docs/
├── logs/
├── requirements.txt
└── README.md
```

## Implementation Roadmap

The project is planned across five weeks:

1. Repository organization, dataset exploration, and AWS S3 ingestion.
2. PySpark, Databricks, and Delta Lake implementation.
3. Apache Airflow workflow orchestration.
4. Snowflake data warehousing and dbt transformations.
5. End-to-end integration, testing, CI/CD, and documentation.

## Project Status

**Current Phase:** Repository organization and initial dataset exploration.

Technologies and capabilities will be marked as implemented only after their working implementation has been completed and verified.

## Engineering Approach

The primary objective is to demonstrate practical implementation of modern Data Engineering tools and architecture.

The project will retain the original source dataset as its baseline. Data validation and pipeline reliability mechanisms will be implemented as engineering controls, while the main focus remains on ingestion, processing, orchestration, storage, and analytical transformation.

## Licence and Attribution

The source dataset is licensed under CC BY-NC 4.0. Its attribution and licence terms must be respected when using or redistributing the dataset and project materials.