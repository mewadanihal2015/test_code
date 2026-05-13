import os
import zipfile
from datetime import datetime
from cryptography.fernet import Fernet
import base64
import hashlib

# ==========================================
# CONFIG
# ==========================================

SOURCE_FOLDER = r"C:\GameSaves"
BACKUP_FOLDER = r"C:\EncryptedBackups"

PASSWORD = "YourStrongPassword123"

# ==========================================
# KEY GENERATION
# ==========================================

def generate_key(password):

    key = hashlib.sha256(password.encode()).digest()

    return base64.urlsafe_b64encode(key)

# ==========================================
# CREATE ZIP
# ==========================================

def create_zip(source_folder, output_zip):

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:

        for root, dirs, files in os.walk(source_folder):

            for file in files:

                full_path = os.path.join(root, file)

                arcname = os.path.relpath(full_path, source_folder)

                zipf.write(full_path, arcname)

# ==========================================
# ENCRYPT FILE
# ==========================================

def encrypt_file(file_path, key):

    fernet = Fernet(key)

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    encrypted_path = file_path + ".enc"

    with open(encrypted_path, "wb") as f:
        f.write(encrypted)

    os.remove(file_path)

    return encrypted_path

# ==========================================
# MAIN BACKUP PROCESS
# ==========================================

def backup():

    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    zip_name = f"backup_{timestamp}.zip"

    zip_path = os.path.join(BACKUP_FOLDER, zip_name)

    print("Creating zip archive...")
    create_zip(SOURCE_FOLDER, zip_path)

    print("Encrypting archive...")
    key = generate_key(PASSWORD)

    encrypted_file = encrypt_file(zip_path, key)

    print(f"Encrypted backup created:\n{encrypted_file}")

# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    backup()
