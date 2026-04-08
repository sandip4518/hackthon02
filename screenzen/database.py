"""
Database manager for ScreenZen.
Uses SQLite to store screenshot metadata, OCR text, and tags.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """Manages the SQLite database for screenshot storage."""

    def __init__(self, db_path: str = None):
        if db_path is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, "screenzen.db")

        self.db_path = db_path
        self._create_tables()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _create_tables(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS screenshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_path TEXT NOT NULL,
                stored_path TEXT NOT NULL,
                thumbnail_path TEXT,
                ocr_text TEXT DEFAULT '',
                tags TEXT DEFAULT '[]',
                file_size INTEGER DEFAULT 0,
                width INTEGER DEFAULT 0,
                height INTEGER DEFAULT 0,
                date_added TEXT NOT NULL,
                date_modified TEXT NOT NULL,
                is_processed INTEGER DEFAULT 0,
                notes TEXT DEFAULT ''
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        # Create FTS virtual table for full-text search
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS screenshots_fts
            USING fts5(filename, ocr_text, tags, notes, content='screenshots', content_rowid='id')
        """)

        # Triggers to keep FTS in sync
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS screenshots_ai AFTER INSERT ON screenshots BEGIN
                INSERT INTO screenshots_fts(rowid, filename, ocr_text, tags, notes)
                VALUES (new.id, new.filename, new.ocr_text, new.tags, new.notes);
            END
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS screenshots_ad AFTER DELETE ON screenshots BEGIN
                INSERT INTO screenshots_fts(screenshots_fts, rowid, filename, ocr_text, tags, notes)
                VALUES ('delete', old.id, old.filename, old.ocr_text, old.tags, old.notes);
            END
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS screenshots_au AFTER UPDATE ON screenshots BEGIN
                INSERT INTO screenshots_fts(screenshots_fts, rowid, filename, ocr_text, tags, notes)
                VALUES ('delete', old.id, old.filename, old.ocr_text, old.tags, old.notes);
                INSERT INTO screenshots_fts(rowid, filename, ocr_text, tags, notes)
                VALUES (new.id, new.filename, new.ocr_text, new.tags, new.notes);
            END
        """)

        conn.commit()
        conn.close()

    def add_screenshot(self, filename: str, original_path: str, stored_path: str,
                       thumbnail_path: str = "", file_size: int = 0,
                       width: int = 0, height: int = 0) -> int:
        """Add a new screenshot to the database. Returns the new row ID."""
        now = datetime.now().isoformat()
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO screenshots (filename, original_path, stored_path, thumbnail_path,
                                     file_size, width, height, date_added, date_modified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (filename, original_path, stored_path, thumbnail_path,
              file_size, width, height, now, now))

        row_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return row_id

    def update_ocr_result(self, screenshot_id: int, ocr_text: str, tags: List[str]):
        """Update OCR results for a screenshot."""
        now = datetime.now().isoformat()
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE screenshots
            SET ocr_text = ?, tags = ?, is_processed = 1, date_modified = ?
            WHERE id = ?
        """, (ocr_text, json.dumps(tags), now, screenshot_id))

        conn.commit()
        conn.close()

    def get_screenshot(self, screenshot_id: int) -> Optional[Dict]:
        """Get a single screenshot by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM screenshots WHERE id = ?", (screenshot_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return self._row_to_dict(row)
        return None

    def get_all_screenshots(self) -> List[Dict]:
        """Get all screenshots, newest first."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM screenshots ORDER BY date_added DESC")
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_dict(row) for row in rows]

    def get_unprocessed_screenshots(self) -> List[Dict]:
        """Get screenshots that haven't been OCR processed yet."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM screenshots WHERE is_processed = 0")
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_dict(row) for row in rows]

    def search_screenshots(self, query: str) -> List[Dict]:
        """Full-text search across screenshots."""
        if not query.strip():
            return self.get_all_screenshots()

        conn = self._get_connection()
        cursor = conn.cursor()

        # Use FTS5 for fast full-text search
        search_query = " OR ".join(f'"{word}"' for word in query.split())

        try:
            cursor.execute("""
                SELECT s.* FROM screenshots s
                INNER JOIN screenshots_fts fts ON s.id = fts.rowid
                WHERE screenshots_fts MATCH ?
                ORDER BY s.date_added DESC
            """, (search_query,))
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            # Fallback to LIKE search if FTS fails
            like_query = f"%{query}%"
            cursor.execute("""
                SELECT * FROM screenshots
                WHERE filename LIKE ? OR ocr_text LIKE ? OR tags LIKE ? OR notes LIKE ?
                ORDER BY date_added DESC
            """, (like_query, like_query, like_query, like_query))
            rows = cursor.fetchall()

        conn.close()
        return [self._row_to_dict(row) for row in rows]

    def get_all_tags(self) -> Dict[str, int]:
        """Get all unique tags with their counts."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tags FROM screenshots WHERE tags != '[]'")
        rows = cursor.fetchall()
        conn.close()

        tag_counts = {}
        for row in rows:
            try:
                tags = json.loads(row["tags"])
                for tag in tags:
                    tag = tag.strip().lower()
                    if tag:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
            except (json.JSONDecodeError, TypeError):
                continue

        return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True))

    def get_dates(self) -> List[str]:
        """Get unique dates for date grouping."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT DATE(date_added) as date_group
            FROM screenshots
            ORDER BY date_group DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [row["date_group"] for row in rows]

    def get_screenshots_by_date(self, date_str: str) -> List[Dict]:
        """Get screenshots for a specific date."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM screenshots
            WHERE DATE(date_added) = ?
            ORDER BY date_added DESC
        """, (date_str,))
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_dict(row) for row in rows]

    def get_screenshots_by_tag(self, tag: str) -> List[Dict]:
        """Get screenshots that have a specific tag."""
        conn = self._get_connection()
        cursor = conn.cursor()
        like_tag = f'%"{tag}"%'
        cursor.execute("""
            SELECT * FROM screenshots
            WHERE tags LIKE ?
            ORDER BY date_added DESC
        """, (like_tag,))
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_dict(row) for row in rows]

    def delete_screenshot(self, screenshot_id: int) -> Optional[Dict]:
        """Delete a screenshot. Returns the deleted record."""
        record = self.get_screenshot(screenshot_id)
        if record:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM screenshots WHERE id = ?", (screenshot_id,))
            conn.commit()
            conn.close()
        return record

    def get_stats(self) -> Dict:
        """Get database statistics."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as total FROM screenshots")
        total = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) as processed FROM screenshots WHERE is_processed = 1")
        processed = cursor.fetchone()["processed"]

        cursor.execute("SELECT COALESCE(SUM(file_size), 0) as total_size FROM screenshots")
        total_size = cursor.fetchone()["total_size"]

        conn.close()

        all_tags = self.get_all_tags()

        return {
            "total_screenshots": total,
            "processed_screenshots": processed,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2) if total_size > 0 else 0,
            "unique_tags": len(all_tags),
            "total_dates": len(self.get_dates())
        }

    def update_notes(self, screenshot_id: int, notes: str):
        """Update notes for a screenshot."""
        now = datetime.now().isoformat()
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE screenshots SET notes = ?, date_modified = ? WHERE id = ?
        """, (notes, now, screenshot_id))
        conn.commit()
        conn.close()

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict:
        """Convert a database row to a dictionary."""
        d = dict(row)
        # Parse tags JSON
        try:
            d["tags_list"] = json.loads(d.get("tags", "[]"))
        except (json.JSONDecodeError, TypeError):
            d["tags_list"] = []
        return d
