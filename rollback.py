
import shutil
import os

def rollback():
    if os.path.exists("anansi_backup"):
        if os.path.exists("anansi"):
            shutil.rmtree("anansi")
        shutil.move("anansi_backup", "anansi")
        print("Rolled back to previous version.")
    else:
        print("No backup found.")

if __name__ == "__main__":
    rollback()
