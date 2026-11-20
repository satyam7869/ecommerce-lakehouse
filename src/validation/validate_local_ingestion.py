from pathlib import Path
import pyarrow.parquet as pq

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

EXPECTED_ROWS = {
    "customers.parquet": 1_000_000,
    "products.parquet": 50_000,
    "sessions.parquet": 7_455_296,
    "orders.parquet": 1_075_683,
    "order_items.parquet": 4_280_732,
    "returns.parquet": 400_293,
    "support_tickets.parquet": 66_938,
}


def validate_local_ingestion():
    print("===== LOCAL INGESTION VALIDATION =====")

    total_rows = 0
    all_valid = True

    for filename, expected_rows in EXPECTED_ROWS.items():
        file_path = RAW_DIR / filename

        if not file_path.exists():
            print(f"MISSING: {filename}")
            all_valid = False
            continue

        if file_path.stat().st_size == 0:
            print(f"EMPTY: {filename}")
            all_valid = False
            continue

        try:
            metadata = pq.read_metadata(file_path)
            actual_rows = metadata.num_rows
            file_size_mb = file_path.stat().st_size / (1024 ** 2)

            if actual_rows != expected_rows:
                print(
                    f"ROW COUNT MISMATCH: {filename} "
                    f"Expected={expected_rows}, Actual={actual_rows}"
                )
                all_valid = False
                continue

            print(
                f"VALID: {filename} | "
                f"Rows={actual_rows:,} | "
                f"Size={file_size_mb:.2f} MiB"
            )

            total_rows += actual_rows

        except Exception as error:
            print(f"INVALID PARQUET: {filename} | {error}")
            all_valid = False

    print("\n===== VALIDATION SUMMARY =====")
    print(f"Total validated rows: {total_rows:,}")
    print("Overall status:", "PASSED" if all_valid else "FAILED")


if __name__ == "__main__":
    validate_local_ingestion()