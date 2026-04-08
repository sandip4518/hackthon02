"""
Drop Zone Widget for ScreenZen.
Provides a visual drag-and-drop / click-to-upload area.
"""

import customtkinter as ctk
from typing import Callable


class DropZone(ctk.CTkFrame):
    """Visual upload zone with drag-drop styling and click handler."""

    def __init__(self, parent, on_click: Callable = None, **kwargs):
        super().__init__(
            parent,
            fg_color="#1e1e2e",
            corner_radius=16,
            border_width=2,
            border_color="#313244",
            height=180,
            **kwargs
        )

        self.on_click_action = on_click
        self.pack_propagate(False)

        # Inner content
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        # Upload icon
        self.icon_label = ctk.CTkLabel(
            inner,
            text="📤",
            font=ctk.CTkFont(size=42),
        )
        self.icon_label.pack(pady=(0, 8))

        # Main text
        self.main_text = ctk.CTkLabel(
            inner,
            text="Drop screenshots here or click to browse",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#cdd6f4",
        )
        self.main_text.pack()

        # Sub text
        self.sub_text = ctk.CTkLabel(
            inner,
            text="Supports PNG, JPG, GIF, BMP, WebP • Multiple files",
            font=ctk.CTkFont(size=11),
            text_color="#6c7086",
        )
        self.sub_text.pack(pady=(4, 0))

        # Browse button
        self.browse_btn = ctk.CTkButton(
            inner,
            text="📂  Browse Files",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#89b4fa",
            hover_color="#74c7ec",
            text_color="#1e1e2e",
            corner_radius=10,
            height=36,
            width=150,
            command=self._on_click,
        )
        self.browse_btn.pack(pady=(12, 0))

        # Hover effects on the entire frame
        for widget in [self, inner, self.icon_label, self.main_text, self.sub_text]:
            widget.bind("<Enter>", self._on_hover_enter)
            widget.bind("<Leave>", self._on_hover_leave)
            widget.bind("<Button-1>", lambda e: self._on_click())

    def _on_click(self):
        """Trigger the upload action."""
        if self.on_click_action:
            self.on_click_action()

    def _on_hover_enter(self, event=None):
        """Visual hover feedback."""
        self.configure(border_color="#89b4fa")
        self.icon_label.configure(text="📥")

    def _on_hover_leave(self, event=None):
        """Reset hover state."""
        self.configure(border_color="#313244")
        self.icon_label.configure(text="📤")

    def set_processing(self, message: str = "Processing..."):
        """Show processing state."""
        self.main_text.configure(text=message)
        self.icon_label.configure(text="⏳")
        self.browse_btn.configure(state="disabled")

    def set_ready(self):
        """Reset to ready state."""
        self.main_text.configure(text="Drop screenshots here or click to browse")
        self.icon_label.configure(text="📤")
        self.browse_btn.configure(state="normal")
