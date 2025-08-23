from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from utils.parser import extract_text_from_file
from utils.embedding import embed_and_store

class MonitorAgent(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(('.pdf', '.docx', '.txt')):
            print(f"Detected change in: {event.src_path}")
            text = extract_text_from_file(event.src_path)
            embed_and_store(text, event.src_path)

def start_monitor(path="uploaded_docs"):
    observer = Observer()
    observer.schedule(MonitorAgent(), path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()