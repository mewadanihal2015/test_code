
import os
import zipfile
import hashlib
import base64
from datetime import datetime
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog, messagebox

# =========================
# ENCRYPTION HELPERS
# =========================

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def create_zip(source_folder, output_zip):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, source_folder)
                zipf.write(full_path, arcname)

def encrypt_file(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    encrypted_path = file_path + ".enc"

    with open(encrypted_path, "wb") as f:
        f.write(encrypted)

    os.remove(file_path)

    return encrypted_path

# =========================
# GUI FUNCTIONS
# =========================

def browse_source():
    folder = filedialog.askdirectory()
    if folder:
        source_var.set(folder)

def browse_backup():
    folder = filedialog.askdirectory()
    if folder:
        backup_var.set(folder)

def run_backup():
    source = source_var.get()
    backup = backup_var.get()
    password = password_var.get()

    if not source or not backup or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        os.makedirs(backup, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_name = f"backup_{timestamp}.zip"

        zip_path = os.path.join(backup, zip_name)

        status_var.set("Creating ZIP archive...")
        root.update()

        create_zip(source, zip_path)

        status_var.set("Encrypting backup...")
        root.update()

        encrypted_file = encrypt_file(zip_path, password)

        status_var.set("Backup completed.")

        messagebox.showinfo(
            "Success",
            f"Encrypted backup created:\n\n{encrypted_file}"
        )

    except Exception as e:
        messagebox.showerror("Backup Failed", str(e))
        status_var.set("Backup failed.")

# =========================
# GUI SETUP
# =========================

root = tk.Tk()
root.title("Encrypted Backup Manager")
root.geometry("600x300")

source_var = tk.StringVar()
backup_var = tk.StringVar()
password_var = tk.StringVar()
status_var = tk.StringVar(value="Ready")

# Source Folder
tk.Label(root, text="Source Folder").pack(anchor="w", padx=10, pady=(10, 0))

source_frame = tk.Frame(root)
source_frame.pack(fill="x", padx=10)

tk.Entry(source_frame, textvariable=source_var).pack(side="left", fill="x", expand=True)
tk.Button(source_frame, text="Browse", command=browse_source).pack(side="left", padx=5)

# Backup Folder
tk.Label(root, text="Backup Folder").pack(anchor="w", padx=10, pady=(10, 0))

backup_frame = tk.Frame(root)
backup_frame.pack(fill="x", padx=10)

tk.Entry(backup_frame, textvariable=backup_var).pack(side="left", fill="x", expand=True)
tk.Button(backup_frame, text="Browse", command=browse_backup).pack(side="left", padx=5)

# Password
tk.Label(root, text="Encryption Password").pack(anchor="w", padx=10, pady=(10, 0))

tk.Entry(root, textvariable=password_var, show="*").pack(fill="x", padx=10)

# Backup Button
tk.Button(
    root,
    text="Create Encrypted Backup",
    command=run_backup,
    height=2
).pack(pady=20)

# Status
tk.Label(root, textvariable=status_var).pack()

root.mainloop()
