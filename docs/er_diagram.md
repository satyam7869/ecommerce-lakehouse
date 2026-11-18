
# E-commerce Lakehouse — Entity Relationship Diagram

## Relationship Overview

This ER diagram represents the proposed relationships between the
seven source tables of the e-commerce dataset.

Primary keys and foreign keys are candidate relationships inferred
from sample schemas and initial inspection. Full-dataset validation
is pending.

```mermaid
erDiagram

    CUSTOMERS {
        string customer_id PK
        date signup_date
        string region
        string segment
        int lifetime_orders
        float lifetime_spend
        string email_domain
    }

    PRODUCTS {
        string product_id PK
        string category
        string subcategory
        float price
        float cost
        string brand
        date launch_date
        float avg_rating
    }

    SESSIONS {
        string session_id PK
        string customer_id FK
        date session_start
        string device
        string channel
        int pages_viewed
        boolean converted
    }

    ORDERS {
        string order_id PK
        string customer_id FK
        string session_id FK
        date order_date
        string status
        int item_count
        float order_total
        string payment_method
    }

    ORDER_ITEMS {
        string order_item_id PK
        string order_id FK
        string product_id FK
        int quantity
        float unit_price
        float line_total
    }

    RETURNS {
        string return_id PK
        string order_id FK
        string order_item_id FK
        string product_id FK
        date return_date
        string reason
        float refund_amount
    }

    SUPPORT_TICKETS {
        string ticket_id PK
        string customer_id FK
        string order_id FK
        date created_date
        string category
        string priority
        string status
        int resolution_days
    }

    CUSTOMERS ||--o{ SESSIONS : has
    CUSTOMERS ||--o{ ORDERS : places
    SESSIONS ||--o{ ORDERS : associates
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : appears_in
    ORDERS ||--o{ RETURNS : has
    ORDER_ITEMS ||--o{ RETURNS : returned_as
    PRODUCTS ||--o{ RETURNS : identifies
    CUSTOMERS ||--o{ SUPPORT_TICKETS : raises
    ORDERS ||--o{ SUPPORT_TICKETS : relates_to
```

## Important Notes

- PK = Candidate Primary Key.
- FK = Candidate Foreign Key.
- `||` means exactly one.
- `o{` means zero or many.
- `|{` means one or many.

## Validation Status

These are proposed relationships, not yet enforced database constraints.

The full dataset must be checked for:
1. Primary-key uniqueness.
2. Foreign-key integrity.
3. Actual relationship cardinality.
4. Nullable foreign-key behavior.
5. Referential consistency across all seven tables.
