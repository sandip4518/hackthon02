"""
Image Manager for ScreenZen.
Handles image import, thumbnail generation, and export.
"""

import os
import shutil
import zipfile
from datetime import datetime
from typing import List, Tuple, Optional
from PIL import Image


class ImageManager:
    """Manages image file operations — import, thumbnails, and export."""

    SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".tif"}
    THUMBNAIL_SIZE = (200, 200)
    PREVIEW_SIZE = (800, 800)

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

        self.data_dir = data_dir
        self.images_dir = os.path.join(data_dir, "images")
        self.thumbnails_dir = os.path.join(data_dir, "thumbnails")

        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.thumbnails_dir, exist_ok=True)

    def import_image(self, source_path: str) -> Optional[dict]:
        """
        Import an image file into ScreenZen storage.
        Returns dict with stored_path, thumbnail_path, width, height, file_size.
        """
        if not os.path.isfile(source_path):
            return None

        ext = os.path.splitext(source_path)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            return None

        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        original_name = os.path.basename(source_path)
        base_name = os.path.splitext(original_name)[0]
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in base_name)
        stored_filename = f"{timestamp}_{safe_name}{ext}"

        stored_path = os.path.join(self.images_dir, stored_filename)
        thumbnail_path = os.path.join(self.thumbnails_dir, f"thumb_{stored_filename}")

        try:
            # Copy image to storage
            shutil.copy2(source_path, stored_path)

            # Get image info
            with Image.open(stored_path) as img:
                width, height = img.size

            # Generate thumbnail
            self._create_thumbnail(stored_path, thumbnail_path)

            file_size = os.path.getsize(stored_path)

            return {
                "filename": original_name,
                "stored_path": stored_path,
                "thumbnail_path": thumbnail_path,
                "width": width,
                "height": height,
                "file_size": file_size,
            }

        except Exception as e:
            # Clean up on failure
            for path in [stored_path, thumbnail_path]:
                if os.path.exists(path):
                    os.remove(path)
            raise e

    def _create_thumbnail(self, source_path: str, thumbnail_path: str):
        """Generate a thumbnail for an image."""
        try:
            with Image.open(source_path) as img:
                # Convert if needed
                if img.mode in ("RGBA", "P", "LA"):
                    bg = Image.new("RGB", img.size, (30, 30, 46))
                    if img.mode in ("RGBA", "LA"):
                        bg.paste(img, mask=img.split()[-1])
                    else:
                        bg.paste(img)
                    img = bg
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                img.thumbnail(self.THUMBNAIL_SIZE, Image.LANCZOS)

                # Save with appropriate format
                ext = os.path.splitext(thumbnail_path)[1].lower()
                if ext in (".jpg", ".jpeg"):
                    img.save(thumbnail_path, "JPEG", quality=85)
                else:
                    img.save(thumbnail_path, "PNG")
        except Exception:
            # Fallback: just copy a smaller version
            shutil.copy2(source_path, thumbnail_path)

    def get_preview_image(self, stored_path: str) -> Optional[Image.Image]:
        """Get a preview-sized version of an image."""
        try:
            img = Image.open(stored_path)
            if img.mode in ("RGBA", "P", "LA"):
                bg = Image.new("RGB", img.size, (30, 30, 46))
                if img.mode in ("RGBA", "LA"):
                    bg.paste(img, mask=img.split()[-1])
                else:
                    bg.paste(img)
                img = bg
            elif img.mode != "RGB":
                img = img.convert("RGB")

            img.thumbnail(self.PREVIEW_SIZE, Image.LANCZOS)
            return img
        except Exception:
            return None

    def export_zip(self, screenshots: List[dict], output_path: str) -> str:
        """
        Export selected screenshots as a ZIP file.
        Returns path to the created ZIP file.
        """
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for ss in screenshots:
                stored_path = ss.get("stored_path", "")
                if os.path.isfile(stored_path):
                    arcname = ss.get("filename", os.path.basename(stored_path))
                    zipf.write(stored_path, arcname)

        return output_path

    def delete_image_files(self, stored_path: str, thumbnail_path: str):
        """Delete image and its thumbnail from disk."""
        for path in [stored_path, thumbnail_path]:
            if path and os.path.isfile(path):
                try:
                    os.remove(path)
                except OSError:
                    pass

    def get_storage_usage(self) -> dict:
        """Calculate total storage usage."""
        total_size = 0
        file_count = 0

        for dir_path in [self.images_dir, self.thumbnails_dir]:
            if os.path.isdir(dir_path):
                for f in os.listdir(dir_path):
                    fp = os.path.join(dir_path, f)
                    if os.path.isfile(fp):
                        total_size += os.path.getsize(fp)
                        file_count += 1

        return {
            "total_bytes": total_size,
            "total_mb": round(total_size / (1024 * 1024), 2) if total_size > 0 else 0,
            "file_count": file_count,
        }

    @classmethod
    def is_supported_file(cls, filepath: str) -> bool:
        """Check if a file is a supported image format."""
        ext = os.path.splitext(filepath)[1].lower()
        return ext in cls.SUPPORTED_EXTENSIONS
