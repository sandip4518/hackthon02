"""
Search Bar Widget for ScreenZen.
Provides a modern search input with live filtering.
"""

import customtkinter as ctk
from typing import Callable, Optional


class SearchBar(ctk.CTkFrame):
    """Modern search bar with icon and live search callback."""

    def __init__(self, parent, on_search: Callable[[str], None] = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.on_search = on_search
        self._debounce_id = None

        # Container
        self.container = ctk.CTkFrame(
            self,
            fg_color="#1e1e2e",
            corner_radius=12,
            border_width=1,
            border_color="#313244",
        )
        self.container.pack(fill="x", padx=0, pady=0)

        # Inner layout
        inner = ctk.CTkFrame(self.container, fg_color="transparent")
        inner.pack(fill="x", padx=12, pady=8)

        # Search icon label
        self.icon_label = ctk.CTkLabel(
            inner,
            text="🔍",
            font=ctk.CTkFont(size=16),
            width=30,
        )
        self.icon_label.pack(side="left", padx=(0, 4))

        # Search entry
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._on_text_changed)

        self.entry = ctk.CTkEntry(
            inner,
            textvariable=self.search_var,
            placeholder_text="Search screenshots by content, filename, or tag...",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            fg_color="transparent",
            border_width=0,
            height=36,
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=4)

        # Clear button
        self.clear_btn = ctk.CTkButton(
            inner,
            text="✕",
            width=30,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#45475a",
            font=ctk.CTkFont(size=14),
            command=self.clear_search,
        )
        self.clear_btn.pack(side="right", padx=(4, 0))
        self.clear_btn.pack_forget()  # Hidden initially

        # Result count label
        self.result_label = ctk.CTkLabel(
            self.container,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#6c7086",
        )
        self.result_label.pack(anchor="w", padx=16, pady=(0, 6))
        self.result_label.pack_forget()

    def _on_text_changed(self, *args):
        """Handle live text changes with debouncing."""
        query = self.search_var.get().strip()

        # Show/hide clear button
        if query:
            self.clear_btn.pack(side="right", padx=(4, 0))
        else:
            self.clear_btn.pack_forget()

        # Debounce: wait 300ms after last keystroke
        if self._debounce_id:
            self.after_cancel(self._debounce_id)

        self._debounce_id = self.after(300, self._trigger_search)

    def _trigger_search(self):
        """Trigger the search callback."""
        if self.on_search:
            self.on_search(self.search_var.get().strip())

    def clear_search(self):
        """Clear the search field."""
        self.search_var.set("")
        self.entry.focus()

    def set_result_count(self, count: int, query: str = ""):
        """Update the result count display."""
        if query:
            self.result_label.configure(text=f"  Found {count} result{'s' if count != 1 else ''} for \"{query}\"")
            self.result_label.pack(anchor="w", padx=16, pady=(0, 6))
        else:
            self.result_label.pack_forget()

    def get_query(self) -> str:
        """Get current search query."""
        return self.search_var.get().strip()

    def focus_search(self):
        """Focus the search entry."""
        self.entry.focus()
