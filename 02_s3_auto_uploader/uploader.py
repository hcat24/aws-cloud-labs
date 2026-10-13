import argparse 
from pathlib import Path
import boto3
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from queue import Queue, Empty
import json

parser = argparse.ArgumentParser()
parser.add_argument("--bucket", required=True )
parser.add_argument("--profile",default="cloud-labs")
parser.add_argument("--region",default="eu-central-1")
args=parser.parse_args()

BASE_DIR = Path(__file__).resolve().parent
WATCH_DIR = BASE_DIR / "incoming"

BUCKET_NAME = args.bucket

session = boto3.Session(profile_name=args.profile, region_name=args.region)
s3=session.client("s3")

def upload_file(file_path):
    file_path = Path(file_path)

    relative_path = file_path.relative_to(WATCH_DIR)
    object_key = f"incoming/{relative_path.as_posix()}"

    s3.upload_file(str(file_path), BUCKET_NAME, object_key)

    print(f"Uploaded: {file_path.name} → {object_key}")


class UploadHandler(FileSystemEventHandler):
    def __init__(self):
        self.queue = Queue()
        self.retries = {}
        self.missing = {}
        self.delete_retries = {}
        self.last_delete_check = 0

        state_dir = BASE_DIR / ".uploader-state"
        state_dir.mkdir(exist_ok=True)
        self.history_file = state_dir / f"{BUCKET_NAME}.json"

        if self.history_file.exists():
            history = json.loads(self.history_file.read_text())
            self.uploaded = {
                Path(path): tuple(signature)
                for path, signature in history.items()
            }
        else:
            self.uploaded = {}

    def process_file(self, path):
        self.queue.put(Path(path).resolve())

    def process_next_file(self):
        failures = 0

        try:
            path = self.queue.get_nowait()

            if path in self.retries:
                return

        except Empty:
            now = time.monotonic()
            ready = [
                path
                for path, (_, due) in self.retries.items()
                if due <= now
            ]

            if not ready:
                return

            path = min(ready, key=lambda p: self.retries[p][1])
            failures, _ = self.retries[path]

        try:
            self._process_file(path)
        except Exception as error:
            failures += 1
            delay = min(2 ** min(failures, 6), 60)
            self.retries[path] = (
                failures,
                time.monotonic() + delay,
            )
            print(
                f"Failed: {path.name}: {error}. "
                f"Queued for retry in {delay} seconds."
            )
        else:
            self.retries.pop(path, None)

    def save_history(self, uploaded):
        history = {
            str(path): signature
            for path, signature in uploaded.items()
        }

        temporary = self.history_file.with_suffix(".tmp")
        temporary.write_text(json.dumps(history, indent=2))
        temporary.replace(self.history_file)

    def _process_file(self, path):
        if any(
            part.lower().endswith((".part", ".tmp"))
            for part in path.relative_to(WATCH_DIR).parts
        ):
            return
        try:
            previous = None
            stable_checks = 0

            for _ in range(60):
                details = path.stat()
                signature = (details.st_size, details.st_mtime_ns)

                if signature == previous:
                    stable_checks += 1
                else:
                    stable_checks = 0

                if stable_checks >= 3:
                    break

                previous = signature
                time.sleep(1)
            else:
                raise RuntimeError("File is still changing")

            if self.uploaded.get(path) == signature:
                return

            upload_file(path)

            updated = self.uploaded.copy()
            updated[path] = signature
            self.save_history(updated)
            self.uploaded = updated

        except FileNotFoundError:
            print(f"File no longer exists: {path.name}")

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.dest_path)

    def check_deleted_files(self):
        now = time.monotonic()

        if now - self.last_delete_check < 2:
            return

        self.last_delete_check = now

        if not WATCH_DIR.is_dir():
            return

        for path in list(self.uploaded):
            try:
                path.relative_to(WATCH_DIR)
            except ValueError:
                continue

            try:
                path.stat()
            except FileNotFoundError:
                pass
            except OSError as error:
                print(f"Cannot check {path.name}: {error}")
                continue
            else:
                self.missing.pop(path, None)
                self.delete_retries.pop(path, None)
                continue

            missing_since = self.missing.setdefault(path, now)

            if now - missing_since < 10:
                continue

            failures, due = self.delete_retries.get(path, (0, 0))

            if now < due:
                continue

            key = f"incoming/{path.relative_to(WATCH_DIR).as_posix()}"

            try:
                if not WATCH_DIR.is_dir():
                    return

                if path.exists():
                    continue

                s3.delete_object(Bucket=BUCKET_NAME, Key=key)

                updated = self.uploaded.copy()
                del updated[path]
                self.save_history(updated)
                self.uploaded = updated

                self.missing.pop(path, None)
                self.delete_retries.pop(path, None)
                self.retries.pop(path, None)

                print(f"Deleted from S3: {key}")

            except Exception as error:
                failures += 1
                delay = min(2 ** min(failures, 6), 60)
                self.delete_retries[path] = (
                    failures,
                    time.monotonic() + delay,
                )
                print(f"Deletion failed for {path.name}: {error}")
            


WATCH_DIR.mkdir(parents=True, exist_ok=True)

handler = UploadHandler()

observer = Observer()
observer.schedule(handler, str(WATCH_DIR), recursive=True)
observer.start()

for path in WATCH_DIR.rglob("*"):
    if path.is_file():
        handler.process_file(path)

print(f"Watching: {WATCH_DIR}")
print("Press Ctrl+C to stop.")

try:
    while True:
        handler.process_next_file()
        handler.check_deleted_files()
        time.sleep(0.2)
except KeyboardInterrupt:
    observer.stop()
finally:
    observer.join()