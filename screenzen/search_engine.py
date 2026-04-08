"""
Search Engine for ScreenZen.
Provides search, filter, and grouping functionality.
"""

from typing import List, Dict, Optional
from datetime import datetime
from screenzen.database import DatabaseManager


class SearchEngine:
    """Search and filter interface for screenshots."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def search(self, query: str) -> List[Dict]:
        """Full-text search across filenames, OCR text, tags, and notes."""
        return self.db.search_screenshots(query)

    def filter_by_tag(self, tag: str) -> List[Dict]:
        """Get all screenshots with a specific tag."""
        return self.db.get_screenshots_by_tag(tag)

    def filter_by_date(self, date_str: str) -> List[Dict]:
        """Get all screenshots from a specific date."""
        return self.db.get_screenshots_by_date(date_str)

    def get_grouped_by_date(self, screenshots: List[Dict] = None) -> Dict[str, List[Dict]]:
        """Group screenshots by date."""
        if screenshots is None:
            screenshots = self.db.get_all_screenshots()

        groups = {}
        for ss in screenshots:
            try:
                dt = datetime.fromisoformat(ss["date_added"])
                date_key = dt.strftime("%Y-%m-%d")
                date_label = dt.strftime("%B %d, %Y")
            except (ValueError, KeyError):
                date_key = "Unknown"
                date_label = "Unknown Date"

            if date_key not in groups:
                groups[date_key] = {"label": date_label, "items": []}
            groups[date_key]["items"].append(ss)

        return dict(sorted(groups.items(), reverse=True))

    def get_tag_cloud(self) -> Dict[str, int]:
        """Get all tags with their frequencies."""
        return self.db.get_all_tags()

    def get_available_dates(self) -> List[str]:
        """Get all unique import dates."""
        return self.db.get_dates()
