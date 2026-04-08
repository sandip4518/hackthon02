"""
Confirmation Dialog for ScreenZen.
Ask the user to confirm/rename a newly detected screenshot.
Supports destination folder selection.
"""

import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from typing import Callable, List


class ConfirmationDialog(ctk.CTkToplevel):
    """
    Popup dialog that shows a new screenshot, its OCR text,
    and lets the user rename/confirm before saving.
    """

    def __init__(self, parent, image_path: str, ocr_text: str, tags: List[str],
                 on_confirm: Callable[[str, str], None], on_cancel: Callable):
        super().__init__(parent)

        self.image_path = image_path
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        self.title("New Screenshot Detected! — ScreenZen")
        self.geometry("600x700")
        self.configure(fg_color="#181825")
        self.attributes("-topmost", True)
        self.deiconify()
        self.lift()

        # Layout
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        # Header
        ctk.CTkLabel(
            self,
            text="📸  New Screenshot Found",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#cdd6f4",
        ).pack(pady=(20, 10))

        # Image Preview
        self.preview_frame = ctk.CTkFrame(self, fg_color="#1e1e2e", height=220)
        self.preview_frame.pack(fill="x", padx=20, pady=5)
        self.preview_frame.pack_propagate(False)

        try:
            img = Image.open(image_path)
            img.thumbnail((560, 200), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            ctk.CTkLabel(self.preview_frame, image=self.photo, text="").pack(expand=True)
        except Exception:
            ctk.CTkLabel(self.preview_frame, text="Preview unavailable").pack(expand=True)

        # ── Rename Field ──
        ctk.CTkLabel(
            self,
            text="Name your screenshot:",
            font=ctk.CTkFont(size=13),
            text_color="#a6adc8",
        ).pack(anchor="w", padx=20, pady=(10, 0))

        suggested_name = "screenshot_" + os.path.basename(image_path)
        if tags:
            suggested_name = "_".join(tags[:3])
        elif ocr_text.strip():
            first_line = ocr_text.split("\n")[0].strip()
            suggested_name = "".join(c if c.isalnum() or c==" " else "_" for c in first_line[:30]).strip().replace(" ", "_")

        self.name_var = ctk.StringVar(value=suggested_name)
        self.name_entry = ctk.CTkEntry(
            self,
            textvariable=self.name_var,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#1e1e2e",
            border_color="#313244",
        )
        self.name_entry.pack(fill="x", padx=20, pady=5)
        self.name_entry.focus()

        # ── Destination Field ──
        ctk.CTkLabel(
            self,
            text="Save to folder:",
            font=ctk.CTkFont(size=13),
            text_color="#a6adc8",
        ).pack(anchor="w", padx=20, pady=(10, 0))

        dest_frame = ctk.CTkFrame(self, fg_color="transparent")
        dest_frame.pack(fill="x", padx=20, pady=5)

        # Default to the app's internal library or user's preference if we added one
        default_dest = os.path.join(os.path.expanduser("~"), "Documents", "ScreenZen")
        os.makedirs(default_dest, exist_ok=True)
        
        self.dest_var = ctk.StringVar(value=default_dest)
        self.dest_entry = ctk.CTkEntry(
            dest_frame,
            textvariable=self.dest_var,
            font=ctk.CTkFont(size=12),
            height=36,
            fg_color="#1e1e2e",
            border_color="#313244",
        )
        self.dest_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            dest_frame,
            text="📂",
            width=40,
            height=36,
            fg_color="#313244",
            command=self._browse_dest,
        )
        self.browse_btn.pack(side="right")

        # ── OCR Preview ──
        ctk.CTkLabel(
            self,
            text="Extracted Text Preview:",
            font=ctk.CTkFont(size=13),
            text_color="#a6adc8",
        ).pack(anchor="w", padx=20, pady=(10, 0))

        self.ocr_box = ctk.CTkTextbox(
            self,
            height=80,
            fg_color="#11111b",
            font=ctk.CTkFont(size=11),
            border_color="#313244",
            border_width=1,
        )
        self.ocr_box.pack(fill="x", padx=20, pady=5)
        self.ocr_box.insert("1.0", ocr_text if ocr_text.strip() else "[No text detected]")
        self.ocr_box.configure(state="disabled")

        # ── Action Buttons ──
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)

        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="🚀  Save & Organize",
            fg_color="#a6e3a1",
            hover_color="#94e2d5",
            text_color="#1e1e2e",
            font=ctk.CTkFont(weight="bold", size=14),
            height=48,
            command=self._on_confirm,
        )
        self.save_btn.pack(side="right", expand=True, fill="x", padx=(10, 0))

        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="✕  Discard Original",
            fg_color="#f38ba8",
            hover_color="#eba0ac",
            text_color="#1e1e2e",
            height=48,
            command=self._on_cancel,
        )
        self.cancel_btn.pack(side="left", padx=(0, 10))

    def _browse_dest(self):
        path = filedialog.askdirectory(initialdir=self.dest_var.get())
        if path:
            self.dest_var.set(path)

    def _on_confirm(self):
        new_name = self.name_var.get().strip()
        new_path = self.dest_var.get().strip()
        if not new_name:
            new_name = "unnamed"
        self.on_confirm(new_name, new_path)
        self.destroy()

    def _on_cancel(self):
        self.on_cancel()
        self.destroy()
