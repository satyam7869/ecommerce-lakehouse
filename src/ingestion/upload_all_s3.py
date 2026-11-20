
from pathlib import Path
import hashlib
import logging

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import pyarrow.parquet as pq


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

BUCKET_NAME = "ecommerce-lakehouse-de-2026-101"
REGION = "ap-south-1"

PARQUET_FILES = [
    "customers.parquet",
    "products.parquet",
    "sessions.parquet",
    "orders.parquet",
    "order_items.parquet",
    "returns.parquet",
    "support_tickets.parquet",
]

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "s3_upload.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 without loading the entire file into memory."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def is_valid_parquet(file_path: Path) -> bool:
    """Check whether the local file is a readable, non-empty Parquet file."""
    if not file_path.exists() or file_path.stat().st_size == 0:
        return False

    try:
        metadata = pq.read_metadata(file_path)
        return metadata.num_rows > 0
    except Exception:
        logging.exception("Invalid Parquet file: %s", file_path.name)
        return False


def get_s3_object_sha256(s3_client, s3_key: str):
    """Read the previously stored SHA-256 metadata from S3."""
    try:
        response = s3_client.head_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
        )
        return response.get("Metadata", {}).get("sha256")

    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code")
        status_code = error.response.get(
            "ResponseMetadata", {}
        ).get("HTTPStatusCode")

        if error_code in ("404", "NoSuchKey", "NotFound") or status_code == 404:
            return None

        raise


def upload_all_to_s3():
    retry_config = Config(
        retries={
            "mode": "standard",
            "total_max_attempts": 4,
        }
    )

    s3_client = boto3.client(
        "s3",
        region_name=REGION,
        config=retry_config,
    )

    uploaded_files = []
    skipped_files = []
    failed_files = []

    for filename in PARQUET_FILES:
        local_file = RAW_DIR / filename
        s3_key = f"raw/{local_file.stem}/{filename}"

        try:
            if not is_valid_parquet(local_file):
                raise ValueError(
                    f"Missing, empty, or invalid Parquet file: {filename}"
                )

            local_sha256 = calculate_sha256(local_file)
            remote_sha256 = get_s3_object_sha256(s3_client, s3_key)

            if remote_sha256 == local_sha256:
                print(f"Skipping: {filename} (checksum matches)", flush=True)
                logging.info("SKIPPED - checksum matches: %s", filename)
                skipped_files.append(filename)
                continue

            print(f"Uploading: {filename} ...", flush=True)

            s3_client.upload_file(
                str(local_file),
                BUCKET_NAME,
                s3_key,
                ExtraArgs={
                    "Metadata": {
                        "sha256": local_sha256
                    }
                },
            )

            logging.info("UPLOADED - %s", filename)
            uploaded_files.append(filename)

        except Exception:
            logging.exception("FAILED - %s", filename)
            failed_files.append(filename)

    print("\n========== S3 UPLOAD SUMMARY ==========")
    print(f"Uploaded: {len(uploaded_files)}")
    print(f"Skipped:  {len(skipped_files)}")
    print(f"Failed:   {len(failed_files)}")

    if uploaded_files:
        print("\nUploaded files:", uploaded_files)

    if skipped_files:
        print("\nSkipped files:", skipped_files)

    if failed_files:
        print("\nFailed files:", failed_files)

    print("=======================================")


if __name__ == "__main__":
    upload_all_to_s3()
