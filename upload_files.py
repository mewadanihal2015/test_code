from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import time

UPLOAD_URL = "https://example.com/upload"

class UploadHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            print("Uploading:", event.src_path)

            with open(event.src_path, "rb") as f:
                response = requests.post(
                    UPLOAD_URL,
                    files={"file": f}
                )

            print("Done:", response.status_code)

observer = Observer()
observer.schedule(UploadHandler(), path="files", recursive=False)

observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
