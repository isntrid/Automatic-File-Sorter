import os
import shutil
from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file = event.src_path
        filename = os.path.basename(file)
        extension = os.path.splitext(filename)[1].lower()

        if "#" in filename or extension == ".crdownload":
            return

        if extension in [".jpg", ".jpeg", ".png", ".jfif"]:
            move_file(file, "Images")

        elif extension == ".exe":
            move_file(file, "Executables")

def move_file(file, folder):
    time.sleep(1)

    folder_destination = os.path.join(
        r"C:\Users\ridn1\Downloads", folder
    )

    os.makedirs(folder_destination, exist_ok=True)
    filename = os.path.basename(file)
    destination = os.path.join(folder_destination, filename)

    try:
        shutil.move(file, destination)
        print(f"Moved {filename} → {folder}")
    except FileNotFoundError:
        print(f"File disappeared before it could be moved: {filename}")
    except PermissionError:
        print(f"Could not move: {filename}")

def auto_sort():
    folder_source = r"C:\Users\ridn1\Downloads"

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_source, recursive=False)
    observer.start()

    print("Watching Downloads...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

auto_sort()
