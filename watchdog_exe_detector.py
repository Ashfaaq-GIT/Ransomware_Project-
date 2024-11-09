import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime


DIRECTORY = "/home/project/test"

class Watcher:
    def __init__(self, directory):
        self.directory = directory
        self.observer = Observer()

    def run(self):
        event_handler = EventHandler()
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()
        print(f"Monitoring directory: {self.directory} for any file changes.")
        try:
            while True:
                time.sleep(1)  # Keep the program running
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Trigger when a new file is created"""
        if event.is_directory:
            return
        timestamp = get_current_timestamp()
        print(f"File created: {event.src_path} at {timestamp}")
        show_popup("File Created", event.src_path, timestamp)

    def on_modified(self, event):
        """Trigger when a file is modified"""
        if event.is_directory:
            return
        timestamp = get_current_timestamp()
        print(f"File modified: {event.src_path} at {timestamp}")
        show_popup("File Modified", event.src_path, timestamp)


def get_current_timestamp():
    """Returns the current timestamp in a readable format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def show_popup(event_type, file_path, timestamp):
    """Display a Tkinter popup with event details and timestamp"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

   
    message = f"Event: {event_type}\nFile: {file_path}\nTimestamp: {timestamp}"
    
    
    messagebox.showinfo("File Event", message)
    
    root.destroy()  # Destroy the Tkinter root window after the message box is closed


if __name__ == "__main__":
    watcher = Watcher(DIRECTORY)
    watcher.run()

