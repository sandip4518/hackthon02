"""
Sidebar Widget for ScreenZen.
Shows stats, tag cloud, and date filters.
"""

import customtkinter as ctk
from typing import Callable, Dict, List, Optional


class Sidebar(ctk.CTkFrame):
    """
    Left sidebar with dashboard stats, tag cloud, and date groups.
    """

    def __init__(self, parent,
                 on_tag_click: Callable[[str], None] = None,
                 on_date_click: Callable[[str], None] = None,
                 on_show_all: Callable[[], None] = None,
                 **kwargs):
        super().__init__(
            parent,
            fg_color="#11111b",
            corner_radius=0,
            width=260,
            **kwargs
        )

        self.on_tag_click = on_tag_click
        self.on_date_click = on_date_click
        self.on_show_all = on_show_all

        self.pack_propagate(False)

        # ── Logo / App Title ──
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=16, pady=(20, 4))

        ctk.CTkLabel(
            logo_frame,
            text="🖥️  ScreenZen",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#cdd6f4",
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_frame,
            text="Screenshot Super-Organizer",
            font=ctk.CTkFont(size=11),
            text_color="#6c7086",
        ).pack(anchor="w", pady=(2, 0))

        # Divider
        ctk.CTkFrame(self, fg_color="#313244", height=1).pack(fill="x", padx=16, pady=12)

        # ── Stats Section ──
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkLabel(
            self.stats_frame,
            text="📊  DASHBOARD",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#a6adc8",
        ).pack(anchor="w", pady=(0, 8))

        self.stats_grid = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        self.stats_grid.pack(fill="x")

        self.stat_labels = {}
        stats = [
            ("total", "📸", "Screenshots", "0"),
            ("processed", "🔤", "OCR Done", "0"),
            ("tags", "🏷️", "Tags", "0"),
            ("size", "💾", "Storage", "0 MB"),
        ]

        for i, (key, icon, label, default) in enumerate(stats):
            row = i // 2
            col = i % 2

            stat_card = ctk.CTkFrame(
                self.stats_grid,
                fg_color="#1e1e2e",
                corner_radius=8,
            )
            stat_card.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            self.stats_grid.columnconfigure(col, weight=1)

            ctk.CTkLabel(
                stat_card,
                text=f"{icon} {label}",
                font=ctk.CTkFont(size=10),
                text_color="#6c7086",
            ).pack(padx=8, pady=(6, 0), anchor="w")

            value_label = ctk.CTkLabel(
                stat_card,
                text=default,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#cdd6f4",
            )
            value_label.pack(padx=8, pady=(0, 6), anchor="w")
            self.stat_labels[key] = value_label

        # Divider
        ctk.CTkFrame(self, fg_color="#313244", height=1).pack(fill="x", padx=16, pady=12)

        # ── Show All Button ──
        self.show_all_btn = ctk.CTkButton(
            self,
            text="📋  Show All Screenshots",
            font=ctk.CTkFont(size=13),
            fg_color="#313244",
            hover_color="#45475a",
            corner_radius=8,
            height=36,
            command=self._on_show_all,
        )
        self.show_all_btn.pack(fill="x", padx=16, pady=(0, 8))

        # Divider
        ctk.CTkFrame(self, fg_color="#313244", height=1).pack(fill="x", padx=16, pady=4)

        # ── Tags Section ──
        tags_header = ctk.CTkFrame(self, fg_color="transparent")
        tags_header.pack(fill="x", padx=16, pady=(8, 4))

        ctk.CTkLabel(
            tags_header,
            text="🏷️  TAGS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#a6adc8",
        ).pack(anchor="w")

        self.tags_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=150,
        )
        self.tags_scroll.pack(fill="x", padx=12, pady=(0, 4))

        self.tags_container = ctk.CTkFrame(self.tags_scroll, fg_color="transparent")
        self.tags_container.pack(fill="x")

        self.no_tags_label = ctk.CTkLabel(
            self.tags_container,
            text="No tags yet",
            font=ctk.CTkFont(size=11),
            text_color="#585b70",
        )
        self.no_tags_label.pack(pady=8)

        # Divider
        ctk.CTkFrame(self, fg_color="#313244", height=1).pack(fill="x", padx=16, pady=4)

        # ── Dates Section ──
        dates_header = ctk.CTkFrame(self, fg_color="transparent")
        dates_header.pack(fill="x", padx=16, pady=(8, 4))

        ctk.CTkLabel(
            dates_header,
            text="📅  DATES",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#a6adc8",
        ).pack(anchor="w")

        self.dates_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=120,
        )
        self.dates_scroll.pack(fill="x", padx=12, pady=(0, 8))

        self.dates_container = ctk.CTkFrame(self.dates_scroll, fg_color="transparent")
        self.dates_container.pack(fill="x")

        self.no_dates_label = ctk.CTkLabel(
            self.dates_container,
            text="No dates yet",
            font=ctk.CTkFont(size=11),
            text_color="#585b70",
        )
        self.no_dates_label.pack(pady=8)

        # ── OCR Status ──
        ctk.CTkFrame(self, fg_color="#313244", height=1).pack(fill="x", padx=16, pady=4, side="bottom")

        self.ocr_status_label = ctk.CTkLabel(
            self,
            text="⏳ OCR: checking...",
            font=ctk.CTkFont(size=10),
            text_color="#6c7086",
        )
        self.ocr_status_label.pack(padx=16, pady=(4, 12), anchor="w", side="bottom")

    def update_stats(self, stats: Dict):
        """Update dashboard statistics."""
        self.stat_labels["total"].configure(text=str(stats.get("total_screenshots", 0)))
        self.stat_labels["processed"].configure(text=str(stats.get("processed_screenshots", 0)))
        self.stat_labels["tags"].configure(text=str(stats.get("unique_tags", 0)))
        size_mb = stats.get("total_size_mb", 0)
        self.stat_labels["size"].configure(text=f"{size_mb} MB")

    def update_tags(self, tag_counts: Dict[str, int]):
        """Update the tag cloud."""
        # Clear existing tags
        try:
            for widget in list(self.tags_container.winfo_children()):
                widget.destroy()
        except Exception:
            pass

        if not tag_counts:
            self.no_tags_label = ctk.CTkLabel(
                self.tags_container,
                text="No tags yet",
                font=ctk.CTkFont(size=11),
                text_color="#585b70",
            )
            self.no_tags_label.pack(pady=8)
            return

        # Create tag buttons in a flow layout
        flow_frame = ctk.CTkFrame(self.tags_container, fg_color="transparent")
        flow_frame.pack(fill="x", pady=4)

        # Color palette for tags
        colors = ["#89b4fa", "#a6e3a1", "#f9e2af", "#f38ba8", "#cba6f7",
                   "#94e2d5", "#fab387", "#74c7ec", "#f2cdcd", "#b4befe"]

        row_frame = ctk.CTkFrame(flow_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=1)
        current_width = 0
        max_width = 220

        for i, (tag, count) in enumerate(list(tag_counts.items())[:20]):
            color = colors[i % len(colors)]
            tag_text = f"#{tag} ({count})"
            btn_width = len(tag_text) * 8 + 16

            if current_width + btn_width > max_width:
                row_frame = ctk.CTkFrame(flow_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=1)
                current_width = 0

            btn = ctk.CTkButton(
                row_frame,
                text=tag_text,
                font=ctk.CTkFont(size=10),
                fg_color=color,
                text_color="#1e1e2e",
                hover_color="#bac2de",
                corner_radius=12,
                height=24,
                width=btn_width,
                command=lambda t=tag: self._on_tag_click(t),
            )
            btn.pack(side="left", padx=2, pady=1)
            current_width += btn_width + 4

    def update_dates(self, dates: List[str]):
        """Update the date list."""
        try:
            for widget in list(self.dates_container.winfo_children()):
                widget.destroy()
        except Exception:
            pass

        if not dates:
            self.no_dates_label = ctk.CTkLabel(
                self.dates_container,
                text="No dates yet",
                font=ctk.CTkFont(size=11),
                text_color="#585b70",
            )
            self.no_dates_label.pack(pady=8)
            return

        for date_str in dates[:15]:
            btn = ctk.CTkButton(
                self.dates_container,
                text=f"📅  {date_str}",
                font=ctk.CTkFont(size=11),
                fg_color="transparent",
                text_color="#bac2de",
                hover_color="#1e1e2e",
                anchor="w",
                height=28,
                corner_radius=6,
                command=lambda d=date_str: self._on_date_click(d),
            )
            btn.pack(fill="x", pady=1)

    def set_ocr_status(self, status: str):
        """Update OCR engine status."""
        self.ocr_status_label.configure(text=f"OCR: {status}")

    def _on_tag_click(self, tag: str):
        if self.on_tag_click:
            self.on_tag_click(tag)

    def _on_date_click(self, date_str: str):
        if self.on_date_click:
            self.on_date_click(date_str)

    def _on_show_all(self):
        if self.on_show_all:
            self.on_show_all()
