import time, csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from entropy import calculate_entropy
from config import *

file_events = []

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.check(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.check(event.src_path)

    def check(self, path):
        now = time.time()
        file_events.append(now)

        recent = [t for t in file_events if now - t < TIME_WINDOW]
        entropy = calculate_entropy(path)

        reasons = []

        if len(recent) > MAX_FILE_CHANGES:
            reasons.append("Rapid file modifications")

        if entropy > ENTROPY_THRESHOLD:
            reasons.append("High entropy detected")

        if path.endswith(SUSPICIOUS_EXTENSION):
            reasons.append("Suspicious extension detected")

        if reasons:
            print("\n⚠️ RANSOMWARE SUSPECTED")
            for r in reasons:
                print("-", r)

            with open("logs/activity_log.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([time.ctime(), path, entropy, ";".join(reasons)])

if __name__ == "__main__":
    print("🔍 Monitoring started...")
    observer = Observer()
    observer.schedule(Handler(), "monitored_folder", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
