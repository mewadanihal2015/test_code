import os
import tempfile
import shutil

def atomic_write(file_path, data):
    dir_name = os.path.dirname(file_path) or "."
    
    with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_name) as tmp:
        tmp.write(data)
        temp_name = tmp.name

    shutil.move(temp_name, file_path)
