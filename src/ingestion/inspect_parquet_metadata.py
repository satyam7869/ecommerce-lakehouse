
from huggingface_hub import hf_hub_download
import pyarrow.parquet as pq


REPO_ID = "HariJha/FreeEcommerceTwin14M"
FILE_NAME = "customers.parquet"


def inspect_parquet_metadata():

    print("Downloading customers.parquet...")

    file_path = hf_hub_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        filename=FILE_NAME
    )

    print("\n===== PARQUET METADATA =====")

    metadata = pq.read_metadata(file_path)

    print("Total rows:", metadata.num_rows)
    print("Total row groups:", metadata.num_row_groups)
    print("Total columns:", metadata.num_columns)

    print("\n===== SCHEMA =====")
    print(metadata.schema)

    print("\n===== ROW GROUP DETAILS =====")

    for index in range(metadata.num_row_groups):
        row_group = metadata.row_group(index)

        print(f"\nRow Group {index}")
        print("Rows:", row_group.num_rows)
        print("Columns:", row_group.num_columns)


    print("\n===== COMPRESSION DETAILS =====")

    for index in range(metadata.num_row_groups):
        row_group = metadata.row_group(index)

        print(f"\nRow Group {index}")
        print("Uncompressed size:", row_group.total_byte_size)

        for column_index in range(row_group.num_columns):
            column = row_group.column(column_index)

            print(column.path_in_schema,"->",column.compression)
            print("Compressed:", column.total_compressed_size)
            print("Uncompressed:", column.total_uncompressed_size)

if __name__ == "__main__":
    inspect_parquet_metadata()

