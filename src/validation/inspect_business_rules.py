import pandas as pd
from pathlib import Path

# Load support ticket sample
path = Path("data/samples/support_tickets_sample_50rows.csv")
tickets = pd.read_csv(path)

print("=== TICKET STATUS DISTRIBUTION ===")
print(tickets["status"].value_counts(dropna=False))

print("\n=== RESOLUTION DAYS DISTRIBUTION ===")
print(tickets["resolution_days"].value_counts(dropna=False).sort_index())

print("\n=== STATUS VS RESOLUTION DAYS ===")
print(
    tickets.groupby("status")["resolution_days"]
    .agg(["count", "min", "max", "mean"])
)

# Inspect date formats
date_columns = {
    "customers": ("customers_sample_50rows.csv", "signup_date"),
    "products": ("products_sample_50rows.csv", "launch_date"),
    "orders": ("orders_sample_50rows.csv", "order_date"),
    "sessions": ("sessions_sample_50rows.csv", "session_start"),
    "returns": ("returns_sample_50rows.csv", "return_date"),
    "support_tickets": ("support_tickets_sample_50rows.csv", "created_date")
}

print("\n=== DATE FORMAT INSPECTION ===")

for table, (filename, column) in date_columns.items():
    df = pd.read_csv(Path("data/samples") / filename)

    parsed = pd.to_datetime(df[column], errors="coerce")

    print(f"\nTable: {table}")
    print(f"Column: {column}")
    print(f"Example: {df[column].iloc[0]}")
    print(f"Successfully parsed: {parsed.notna().sum()}/{len(df)}")
    print(f"Minimum date: {parsed.min()}")
    print(f"Maximum date: {parsed.max()}")
