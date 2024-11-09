import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directory to monitor
MONITOR_DIR = "/home/project/test"  # Change this to the directory you want to monitor

# Event handler class that responds to changes
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        """Triggered when a file or directory is modified."""
        if event.is_directory:
            print(f"Directory modified: {event.src_path}")
        else:
            print(f"File modified: {event.src_path}")

    def on_created(self, event):
        """Triggered when a file or directory is created."""
        if event.is_directory:
            print(f"Directory created: {event.src_path}")
        else:
            print(f"File created: {event.src_path}")
            
    def on_deleted(self, event):
        """Triggered when a file or directory is deleted."""
        if event.is_directory:
            print(f"Directory deleted: {event.src_path}")
        else:
            print(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        """Triggered when a file or directory is moved or renamed."""
        print(f"Moved: {event.src_path} -> {event.dest_path}")



def start_monitoring():
    # Created an event handler instance
    event_handler = FileChangeHandler()

    # Created an observer instance and assign the event handler
    observer = Observer()
    observer.schedule(event_handler, MONITOR_DIR, recursive=True)

    # Start monitoring
    observer.start()
    print(f"Monitoring started on {MONITOR_DIR}...")
    
    try:
        while True:
            time.sleep(1)  # Sleep to avoid maxing out the CPU
    except KeyboardInterrupt:
        observer.stop()  # Stop monitoring when user presses Ctrl+C
    observer.join()  # Wait for the observer to finish

if __name__ == "__main__":
    start_monitoring()

