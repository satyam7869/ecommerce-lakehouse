from pathlib import Path
from huggingface_hub import hf_hub_download
import logging
import pyarrow.parquet as pq

def is_valid_parquet(file_path):
    if not file_path.exists():
        return False

    if file_path.stat().st_size == 0:
        return False

    try:
        pq.read_metadata(file_path)
        return True

    except Exception:
        return False

REPO_ID = "HariJha/FreeEcommerceTwin14M"

PARQUET_FILES = [
    "customers.parquet",
    "products.parquet",
    "sessions.parquet",
    "orders.parquet",
    "order_items.parquet",
    "returns.parquet",
    "support_tickets.parquet",
]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "ingestion.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",s
    filemode="a"
)

def download_parquet_files():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    failed_files = []
    successful_files = []
    skipped_files = []

    logging.info("========== NEW INGESTION RUN ==========")

    for filename in PARQUET_FILES:
        file_path = RAW_DIR / filename

        try:
            if is_valid_parquet(file_path):
                logging.info("Skipping valid existing file: %s", filename)
                skipped_files.append(filename)
                continue

            logging.info("Downloading: %s", filename)

            downloaded_path = hf_hub_download(
                repo_id=REPO_ID,
                repo_type="dataset",
                filename=filename,
                local_dir=str(RAW_DIR)
            )

            if not is_valid_parquet(Path(downloaded_path)):
                raise ValueError("Downloaded file failed Parquet validation")

            logging.info("Downloaded and validated: %s", filename)
            successful_files.append(filename)

        except Exception:
            logging.exception("Download failed: %s", filename)
            failed_files.append(filename)

    logging.info("Ingestion process completed")
    logging.info("Downloaded: %s", successful_files)
    logging.info("Skipped: %s", skipped_files)
    logging.info("Failed: %s", failed_files)

    print("\n===== INGESTION SUMMARY =====")
    print("Downloaded:", len(successful_files))
    print("Skipped:", len(skipped_files))
    print("Failed:", len(failed_files))


if __name__ == "__main__":
    download_parquet_files()