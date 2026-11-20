
from huggingface_hub import HfApi

REPO_ID = "HariJha/FreeEcommerceTwin14M"


def inspect_remote_dataset():
    api = HfApi()

    print("Connecting to Hugging Face...")
    
    files = list(
        api.list_repo_tree(
            repo_id=REPO_ID,
            repo_type="dataset",
            recursive=True
        )
    )

    parquet_files = [
        file for file in files
        if getattr(file, "path", "").endswith(".parquet")
    ]

    total_bytes = 0

    print("\n===== REMOTE PARQUET INVENTORY =====")

    for file in sorted(parquet_files, key=lambda x: x.path):
        size = getattr(file, "size", None)

        if size is None:
            print(f"{file.path}: Size unavailable")
            continue

        total_bytes += size
        size_mb = size / (1024 * 1024)

        print(
            f"{file.path:25} "
            f"{size:>12,} bytes "
            f"({size_mb:.2f} MiB)"
        )

    print("\n===== DATASET SUMMARY =====")
    print("Parquet files:", len(parquet_files))
    print(f"Total size: {total_bytes / (1024 * 1024):.2f} MiB")
    print(f"Total size: {total_bytes / (1024 ** 3):.3f} GiB")


if __name__ == "__main__":
    inspect_remote_dataset()
