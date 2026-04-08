"""
Background Listener for ScreenZen.
Monitors the user's Screenshots directory for new images.
"""

import os
import time
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ScreenshotHandler(FileSystemEventHandler):
    """
    Handles file system events for the Screenshots folder.
    """

    SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".png"}

    def __init__(self, on_new_screenshot: Callable[[str], None]):
        self.on_new_screenshot = on_new_screenshot
        self._last_event_time = 0

    def on_created(self, event):
        """Called when a file is created."""
        if event.is_directory:
            return

        filepath = event.src_path
        ext = os.path.splitext(filepath)[1].lower()

        if ext in self.SUPPORTED_EXTENSIONS:
            # Debounce: wait a bit for file to be fully written
            time.sleep(0.5)
            self.on_new_screenshot(filepath)


class ScreenshotWatcher:
    """
    Watches the Windows Screenshots folder for new captures.
    """

    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.observer = None

    def start(self):
        """Start monitoring all potential screenshot folders."""
        possible_dirs = [
            os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots"),
            os.path.join(os.path.expanduser("~"), "OneDrive", "Pictures", "Screenshots"),
            os.path.join(os.path.expanduser("~"), "OneDrive - Personal", "Pictures", "Screenshots"),
            # Some versions of Snip & Sketch save here
            os.path.join(os.path.expanduser("~"), "Videos", "Captures"),
        ]

        self.observer = Observer()
        monitored_count = 0

        for d in possible_dirs:
            if os.path.exists(d):
                event_handler = ScreenshotHandler(self.callback)
                self.observer.schedule(event_handler, d, recursive=False)
                print(f"[Watcher] Now monitoring: {d}")
                monitored_count += 1

        if monitored_count > 0:
            self.observer.start()
        else:
            print("[Watcher] WARNING: No screenshot folders found to monitor.")

    def stop(self):
        """Stop monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
