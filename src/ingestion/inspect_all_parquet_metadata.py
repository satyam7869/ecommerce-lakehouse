from pathlib import Path
import pyarrow.parquet as pq

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def inspect_all_parquet_metadata():
    parquet_files = sorted(RAW_DIR.glob("*.parquet"))

    print("===== PARQUET METADATA REPORT =====")

    for file_path in parquet_files:
        metadata = pq.read_metadata(file_path)

        print(f"\nTable: {file_path.name}")
        print(f"Rows: {metadata.num_rows:,}")
        print(f"Columns: {metadata.num_columns}")
        print(f"Row groups: {metadata.num_row_groups}")
        print(
            f"File size: "
            f"{file_path.stat().st_size / (1024 ** 2):.2f} MiB"
        )

        codecs = set()

        for row_group_index in range(metadata.num_row_groups):
            row_group = metadata.row_group(row_group_index)

            for column_index in range(row_group.num_columns):
                column = row_group.column(column_index)
                codecs.add(column.compression)

        print(f"Compression codecs: {', '.join(sorted(codecs))}")
        print("Schema:")
        print(metadata.schema)


if __name__ == "__main__":
    inspect_all_parquet_metadata()