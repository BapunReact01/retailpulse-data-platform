import os
from huggingface_hub import hf_hub_download
from huggingface_hub import snapshot_download

# Create directory if not exists
output_dir = "data/large_dataset"
os.makedirs(output_dir, exist_ok=True)

print("Starting download of FreeEcommerceTwin14M dataset...")
print("This may take a while as the dataset is ~184 MB")
print("=" * 60)

# Download the entire dataset
dataset_id = "ziadatalabs/FreeEcommerceTwin14M"

try:
    # Download all files from the dataset
    downloaded_path = snapshot_download(
        repo_id=dataset_id,
        repo_type="dataset",
        local_dir=output_dir,
        local_dir_use_symlinks=False
    )
    
    print("=" * 60)
    print("✅ Download complete!")
    print(f"Files downloaded to: {downloaded_path}")
    print("\nDownloaded files:")
    
    # List downloaded files
    for file in os.listdir(downloaded_path):
        file_path = os.path.join(downloaded_path, file)
        if os.path.isfile(file_path):
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"  - {file} ({size_mb:.2f} MB)")
    
    print("\nYou can now load these Parquet files using PySpark!")
    
except Exception as e:
    print(f"❌ Error downloading dataset: {e}")
    print("\nAlternative: Download manually from:")
    print("https://huggingface.co/datasets/ziadatalabs/FreeEcommerceTwin14M")
    