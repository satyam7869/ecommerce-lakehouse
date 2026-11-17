# Dataset Exploration & Profiling

## 1. Overview

This module documents the initial exploration and profiling of the FreeEcommerceTwin14M e-commerce dataset.

The objective was to understand the dataset structure, inspect individual tables, identify column data types, and evaluate basic data-quality characteristics before implementing the Data Engineering pipeline.

## 2. Dataset Source

- **Dataset:** FreeEcommerceTwin14M
- **Provider:** Hugging Face
- **Repository:** HariJha/FreeEcommerceTwin14M
- **Source:** https://huggingface.co/datasets/HariJha/FreeEcommerceTwin14M
- **Format:** CSV samples and Parquet files
- **Total records:** 14,328,942
- **Number of tables:** 7
- **Dataset licence:** CC BY-NC 4.0

The dataset is synthetic and designed with relational consistency and financial reconciliation characteristics.

## 3. Available Tables

| Table | Records |
|---|---:|
| customers | 1,000,000 |
| products | 50,000 |
| sessions | 7,455,296 |
| orders | 1,075,683 |
| order_items | 4,280,732 |
| returns | 400,293 |
| support_tickets | 66,938 |

## 4. Tools Used

- Python
- Pandas
- VS Code

## 5. Exploration Activities

Initial exploration was performed using 50-row CSV samples from each table.

The customers sample was used to practise:

- Dataset shape and column inspection
- Data-type identification
- Missing-value analysis
- Duplicate-row and duplicate-key checks
- Descriptive statistics
- Date-column inspection and conversion
- Basic business-rule investigation

## 6. Initial Observations

Based on the 50-row customers sample:

- Dataset contained 50 rows and 7 columns.
- No null values were observed.
- No complete duplicate rows were observed.
- No duplicate customer IDs were observed.
- `signup_date` was initially represented as an object column.
- `lifetime_orders` was an integer column.
- `lifetime_spend` was a floating-point column.
- No negative lifetime-spend values were observed.
- Some customers had zero lifetime orders and zero lifetime spend.

## 7. Important Limitations

These findings represent only the 50-row customers sample.

They must not be interpreted as results for the complete 1-million-row customers table or the entire 14.3-million-record dataset.

Full-scale validation and processing will be performed separately using PySpark.

## 8. Purpose in the Overall Project

This exploration phase establishes an understanding of the source data before implementing:

- AWS S3 ingestion
- PySpark distributed processing
- Delta Lake architecture
- Apache Airflow orchestration
- Snowflake data warehousing
- dbt transformations

The main project focuses on end-to-end Data Engineering implementation rather than making data cleaning the primary objective.