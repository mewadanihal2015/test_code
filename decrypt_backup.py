from cryptography.fernet import Fernet
import base64
import hashlib

PASSWORD = "YourStrongPassword123"

ENCRYPTED_FILE = r"C:\EncryptedBackups\backup.enc"

OUTPUT_FILE = r"C:\EncryptedBackups\restored_backup.zip"

def generate_key(password):

    key = hashlib.sha256(password.encode()).digest()

    return base64.urlsafe_b64encode(key)

key = generate_key(PASSWORD)

fernet = Fernet(key)

with open(ENCRYPTED_FILE, "rb") as f:
    encrypted_data = f.read()

decrypted = fernet.decrypt(encrypted_data)

with open(OUTPUT_FILE, "wb") as f:
    f.write(decrypted)

print("Backup restored.")
