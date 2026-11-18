# E-commerce Lakehouse — Data Dictionary

## 1. Dataset Overview

- **Dataset:** FreeEcommerceTwin14M
- **Source:** [HariJha/FreeEcommerceTwin14M](https://huggingface.co/datasets/HariJha/FreeEcommerceTwin14M)
- **Total records:** 14,328,942
- **Tables:** 7
- **Format:** Parquet
- **Dataset type:** Synthetic e-commerce data
- **License:** CC BY-NC 4.0

This document describes the initial schema and business-rule observations based on 50-row sample CSV files per table.

**Important:** Sample-level observations are not proof of full-dataset integrity. Primary keys, foreign keys, nullability, and business rules must be validated against the complete dataset before production enforcement.

## 2. Evidence Classification

- **Observed:** Directly verified from sample inspection.
- **Proposed:** Inferred from column names and business context.
- **Pending validation:** Requires verification against the complete dataset or source documentation.

## 3. Customers

| Column | Observed Type | Description | Notes |
|---|---|---|---|
| customer_id | object | Unique customer identifier | Candidate PK |
| signup_date | object | Customer registration date | Date parsing successful in sample |
| region | object | Customer geographic region | Categorical |
| segment | object | Customer segment | Categorical |
| lifetime_orders | int64 | Number of lifetime orders | Non-negative in sample |
| lifetime_spend | float64 | Customer lifetime spending | Currency and calculation semantics unverified |
| email_domain | object | Customer email provider domain | Categorical |

**Sample observations:**
- No duplicate customer IDs.
- No null values.
- Customers with zero orders and zero spend exist; this is not automatically an anomaly.

## 4. Products

| Column | Observed Type | Description | Notes |
|---|---|---|---|
| product_id | object | Product identifier | Candidate PK |
| category | object | Product category | Categorical |
| subcategory | object | Product subcategory | Categorical |
| price | float64 | Product selling/list price | Positive in sample |
| cost | float64 | Product cost | Positive in sample |
| brand | object | Product brand | Categorical |
| launch_date | object | Product launch date | Date parsing successful |
| avg_rating | float64 | Average product rating | Values between 0 and 5 in sample |

**Sample observations:**
- No duplicate product IDs.
- No null values.
- No product with price below cost in the sample.
- Price versus cost should not be enforced as a universal constraint without business confirmation.

## 5. Sessions

| Column | Observed Type | Description | Notes |
|---|---|---|---|
| session_id | object | Session identifier | Candidate PK |
| customer_id | object | Customer associated with session | Candidate FK |
| session_start | object | Session start date/time | Sample values appear date-only |
| device | object | Device used | Categorical |
| channel | object | Acquisition channel | Categorical |
| pages_viewed | int64 | Number of pages viewed | Positive in sample |
| converted | bool | Whether session converted | Boolean |

**Sample observations:**
- No duplicate session IDs.
- No null values.
- 9 of 50 sessions were marked converted.

## 6. Orders

| Column | Observed Type | Description | Notes |
|---|---|---|---|
| order_id | object | Order identifier | Candidate PK |
| customer_id | object | Customer who placed the order | Candidate FK |
| session_id | object | Associated browsing session | Candidate FK |
| order_date | object | Order date | Date parsing successful |
| status | object | Order status | Categorical |
| item_count | int64 | Number of order-item lines, provisionally | Sample evidence; pending full validation |
| order_total | float64 | Order monetary total | Currency and business semantics unverified |
| payment_method | object | Payment method | Categorical |

**Sample observations:**
- No duplicate order IDs.
- One cancelled order had a positive order total.
- `item_count` matched the number of distinct order-item lines for 15 of 16 comparable sampled orders. This is evidence, not a confirmed global rule.

## 7. Order Items

| Column | Observed Type | Description | Notes |
|---|---|---|---|
| order_item_id | object | Order line identifier | Candidate PK |
| order_id | object | Associated order | Candidate FK |
| product_id | object | Purchased product | Candidate FK |
| quantity | int64 | Quantity purchased | Positive in sample |
| unit_price | float64 | Price per unit | Positive in sample |
| line_total | float64 | Total value of order line | Matched quantity × unit_price in 50/50 sample rows |

**Sample observations:**
- No duplicate order-item IDs.
- No null values.
- All 50 sampled line totals matched quantity multiplied by unit price.

## 8. Returns

| Column | Observed Type | Description | Notes |
|---|---|---|---|
| return_id | object | Return identifier | Candidate PK |
| order_id | object | Associated order | Candidate FK |
| order_item_id | object | Associated order line | Candidate FK |
| product_id | object | Returned product | Candidate FK |
| return_date | object | Return date | Date parsing successful |
| reason | object | Return reason | Categorical |
| refund_amount | float64 | Refund amount | Positive in sample |

**Sample observations:**
- No duplicate return IDs.
- No null values.
- 50 sampled return records referenced 42 distinct orders.
- Only 3 of 50 sampled return records matched the 50-row order-item sample. This is insufficient to conclude referential-integrity failures because the samples cover only a small part of the parent table.

## 9. Support Tickets

| Column | Observed Type | Description | Notes |
|---|---|---|---|
| ticket_id | object | Support ticket identifier | Candidate PK |
| customer_id | object | Customer associated with ticket | Candidate FK |
| order_id | object | Associated order | Candidate FK; nullability pending validation |
| created_date | object | Ticket creation date | Date parsing successful |
| category | object | Ticket category | Categorical |
| priority | object | Ticket priority | Categorical |
| status | object | Ticket status | Categorical |
| resolution_days | int64 | Ticket resolution duration | -1 appears to represent unresolved tickets |

**Sample observations:**
- No duplicate ticket IDs.
- No null values in the sample.
- All `open` and `in_progress` tickets had resolution_days = -1.
- All `resolved` and `closed` tickets had positive resolution days.
- The -1 sentinel interpretation requires full-dataset/source validation.

## 10. Candidate Primary Keys

| Table | Candidate Primary Key |
|---|---|
| customers | customer_id |
| products | product_id |
| sessions | session_id |
| orders | order_id |
| order_items | order_item_id |
| returns | return_id |
| support_tickets | ticket_id |

These keys had zero duplicates in their respective 50-row samples. Full-table uniqueness is pending validation.

## 11. Candidate Foreign-Key Relationships

| Child Table | Candidate Foreign Key | Parent Table |
|---|---|---|
| sessions | customer_id | customers |
| orders | customer_id | customers |
| orders | session_id | sessions |
| order_items | order_id | orders |
| order_items | product_id | products |
| returns | order_id | orders |
| returns | order_item_id | order_items |
| returns | product_id | products |
| support_tickets | customer_id | customers |
| support_tickets | order_id | orders |

These relationships are proposed based on schema and business context. Full-dataset referential-integrity checks are pending.

## 12. Data Engineering Validation Plan

The complete dataset will be checked for:

1. Primary-key uniqueness.
2. Foreign-key integrity.
3. Nullability and missing values.
4. Data type and date parsing consistency.
5. Numeric range validation.
6. Order-item reconciliation.
7. Return-to-order-item consistency.
8. Support-ticket resolution rules.
9. Duplicate and unexpected records.

Raw source data will be preserved in the Bronze layer. Type standardization and validated business rules will be implemented in subsequent processing layers.

## 13. Sample Limitations

- Each sample contains only 50 records.
- Sample uniqueness does not prove full-table uniqueness.
- Missing parent records in a sample do not prove broken foreign keys.
- Sample distributions should not be treated as full-dataset statistics.
- Business assumptions must be validated before becoming production constraints.