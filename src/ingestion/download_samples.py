from huggingface_hub import hf_hub_download
import shutil
from pathlib import Path

REPO_ID = "HariJha/FreeEcommerceTwin14M"

TABLES = ["customers", "products", "sessions", "orders", "order_items", "returns", "support_tickets"]

OUTPUT_DIR = Path("data/samples")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for table in TABLES:
    filename = f"{table}_sample_50rows.csv"

    downloaded_path = hf_hub_download(
        repo_id = REPO_ID,
        repo_type = "dataset",
        filename = filename
    )

    shutil.copy(downloaded_path, OUTPUT_DIR / filename)
    print(f"Downloaded: {filename} to {downloaded_path}")
    
    destination_path = OUTPUT_DIR / filename

    if destination_path.exists():
        print(f"File {filename} already exists in {OUTPUT_DIR}. Skipping download.")
    
    else:
        print(f"File {filename} does not exist in {OUTPUT_DIR}. Downloading...")