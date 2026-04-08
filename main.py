"""
ScreenZen — Screenshot Super-Organizer
Entry point for the application.
"""

import sys
import os

# Ensure the project root is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from screenzen.app import ScreenZenApp


def main():
    """Launch the ScreenZen application."""
    app = ScreenZenApp()
    app.mainloop()


if __name__ == "__main__":
    main()
