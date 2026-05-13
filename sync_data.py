import os
import shutil
import hashlib
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

SOURCE_FOLDER = r"C:\GameSaves"
DESTINATION_FOLDER = r"D:\Backup\GameSaves"

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def file_hash(filepath):
    """
    Generate SHA256 hash for file comparison
    """
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def files_are_different(src, dst):
    """
    Compare files using hash
    """
    if not os.path.exists(dst):
        return True

    if os.path.getsize(src) != os.path.getsize(dst):
        return True

    return file_hash(src) != file_hash(dst)


# ==========================================
# SYNC LOGIC
# ==========================================

def sync_folders(source, destination):

    source = Path(source)
    destination = Path(destination)

    for root, dirs, files in os.walk(source):

        relative_path = Path(root).relative_to(source)
        target_dir = destination / relative_path

        # Create missing folders
        target_dir.mkdir(parents=True, exist_ok=True)

        for file in files:

            src_file = Path(root) / file
            dst_file = target_dir / file

            try:
                if files_are_different(src_file, dst_file):

                    shutil.copy2(src_file, dst_file)

                    print(f"[SYNCED] {src_file} -> {dst_file}")

                else:
                    print(f"[SKIPPED] {src_file}")

            except Exception as e:
                print(f"[ERROR] {src_file}: {e}")


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    print("Starting save data sync...\n")

    sync_folders(SOURCE_FOLDER, DESTINATION_FOLDER)

    print("\nSync complete.")
