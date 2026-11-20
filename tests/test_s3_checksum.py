
from pathlib import Path
import hashlib
import boto3

BUCKET_NAME = "ecommerce-lakehouse-de-2026-101"
REGION = "ap-south-1"
TEST_KEY = "raw/checksum-test/checksum_test.txt"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = PROJECT_ROOT / "data" / "checksum_test.txt"


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def main():
    s3 = boto3.client("s3", region_name=REGION)

    original_content = b"ABCDEF"
    modified_content = b"XYZ123"

    # Create original test file
    TEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    TEST_FILE.write_bytes(original_content)

    original_hash = calculate_sha256(TEST_FILE)

    # Upload original content with checksum metadata
    s3.upload_file(
        str(TEST_FILE),
        BUCKET_NAME,
        TEST_KEY,
        ExtraArgs={"Metadata": {"sha256": original_hash}},
    )

    print("Original file uploaded.")
    print("Original size:", TEST_FILE.stat().st_size)
    print("Original SHA-256:", original_hash)

    # Change content without changing file size
    TEST_FILE.write_bytes(modified_content)

    modified_hash = calculate_sha256(TEST_FILE)

    print("\nModified file created.")
    print("Modified size:", TEST_FILE.stat().st_size)
    print("Modified SHA-256:", modified_hash)

    # Read checksum metadata from S3
    response = s3.head_object(
        Bucket=BUCKET_NAME,
        Key=TEST_KEY,
    )

    remote_hash = response.get("Metadata", {}).get("sha256")

    print("\nS3 stored SHA-256:", remote_hash)

    if TEST_FILE.stat().st_size == len(original_content):
        print("Size comparison: SAME")

    if modified_hash != remote_hash:
        print("Checksum comparison: DIFFERENT")
        print("Result: RE-UPLOAD REQUIRED")

        # Upload modified content
        s3.upload_file(
            str(TEST_FILE),
            BUCKET_NAME,
            TEST_KEY,
            ExtraArgs={"Metadata": {"sha256": modified_hash}},
        )

        print("Modified file uploaded successfully.")

        # Verify updated S3 metadata
        updated_response = s3.head_object(
            Bucket=BUCKET_NAME,
            Key=TEST_KEY,
        )

        updated_hash = updated_response.get("Metadata", {}).get("sha256")

        if updated_hash == modified_hash:
            print("SUCCESS: S3 checksum updated and verified.")
        else:
            print("FAILED: S3 checksum verification failed.")


if __name__ == "__main__":
    main()
