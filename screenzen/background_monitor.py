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
        """Start monitoring the screenshots folder."""
        # Standard Windows Screenshots location
        screenshots_dir = os.path.join(
            os.path.expanduser("~"), "Pictures", "Screenshots"
        )

        if not os.path.exists(screenshots_dir):
            try:
                os.makedirs(screenshots_dir, exist_ok=True)
            except Exception:
                print(f"[Watcher] Could not create directory: {screenshots_dir}")
                return

        event_handler = ScreenshotHandler(self.callback)
        self.observer = Observer()
        self.observer.schedule(event_handler, screenshots_dir, recursive=False)
        self.observer.start()
        print(f"[Watcher] Monitoring: {screenshots_dir}")

    def stop(self):
        """Stop monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
