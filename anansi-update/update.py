
import zipfile
import os
import shutil

def apply_update(zip_path, target_dir="anansi"):
    # Backup current version
    if os.path.exists(target_dir):
        shutil.move(target_dir, target_dir + "_backup")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

    print("Update applied.")

if __name__ == "__main__":
    apply_update("anansi-update.zip")
