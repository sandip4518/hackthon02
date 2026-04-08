"""
OCR Engine for ScreenZen.
Uses Tesseract via pytesseract for text extraction from screenshots.
"""

import os
import re
import shutil
from typing import Tuple, List, Optional
from collections import Counter

try:
    import pytesseract
    from PIL import Image, ImageFilter, ImageEnhance
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


# Common Tesseract installation paths on Windows
TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe",
    r"C:\Tesseract-OCR\tesseract.exe",
]

# Common English stop words to filter from tags
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "as", "be", "was", "are",
    "been", "has", "have", "had", "do", "does", "did", "will", "can",
    "could", "would", "should", "may", "might", "shall", "not", "no",
    "this", "that", "these", "those", "i", "you", "he", "she", "we",
    "they", "me", "him", "her", "us", "them", "my", "your", "his",
    "its", "our", "their", "what", "which", "who", "whom", "how",
    "when", "where", "why", "all", "each", "every", "both", "few",
    "more", "most", "other", "some", "such", "than", "too", "very",
    "just", "about", "above", "after", "again", "also", "am", "any",
    "because", "before", "being", "below", "between", "into", "if",
    "then", "there", "here", "so", "up", "out", "off", "over", "under",
    "only", "own", "same", "while", "during", "www", "http", "https",
    "com", "org", "net", "png", "jpg", "jpeg", "gif", "svg",
}


class OCREngine:
    """Tesseract OCR wrapper for text extraction from images."""

    def __init__(self):
        self.is_available = False
        self.tesseract_path = None
        self._setup_tesseract()

    def _setup_tesseract(self):
        """Locate and configure Tesseract OCR."""
        if not TESSERACT_AVAILABLE:
            return

        # Check if tesseract is already in PATH
        if shutil.which("tesseract"):
            self.is_available = True
            return

        # Check common installation paths
        username = os.environ.get("USERNAME", "")
        for path_template in TESSERACT_PATHS:
            path = path_template.format(username) if "{}" in path_template else path_template
            if os.path.isfile(path):
                pytesseract.pytesseract.tesseract_cmd = path
                self.tesseract_path = path
                self.is_available = True
                return

    def extract_text(self, image_path: str) -> str:
        """
        Extract text from an image using Tesseract OCR.
        Returns the extracted text string.
        """
        if not self.is_available:
            return "[OCR unavailable - Tesseract not installed]"

        try:
            img = Image.open(image_path)

            # Convert to RGB if needed
            if img.mode in ("RGBA", "P", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "RGBA" or img.mode == "LA":
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Preprocess for better OCR
            img = self._preprocess_image(img)

            # Run OCR
            text = pytesseract.image_to_string(
                img,
                lang="eng",
                config="--psm 3 --oem 3"
            )

            return text.strip()

        except Exception as e:
            return f"[OCR error: {str(e)}]"

    def _preprocess_image(self, img: Image.Image) -> Image.Image:
        """Preprocess image for better OCR accuracy."""
        # Resize if too small
        min_dim = min(img.size)
        if min_dim < 300:
            scale = 300 / min_dim
            new_size = (int(img.size[0] * scale), int(img.size[1] * scale))
            img = img.resize(new_size, Image.LANCZOS)

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)

        # Sharpen
        img = img.filter(ImageFilter.SHARPEN)

        return img

    @staticmethod
    def extract_tags(ocr_text: str, max_tags: int = 15) -> List[str]:
        """
        Extract meaningful keyword tags from OCR text.
        Filters stop words, short words, and returns most frequent terms.
        """
        if not ocr_text or ocr_text.startswith("[OCR"):
            return []

        # Tokenize: extract words
        words = re.findall(r"[a-zA-Z]{3,}", ocr_text.lower())

        # Filter stop words and very short/long words
        filtered = [
            w for w in words
            if w not in STOP_WORDS and 3 <= len(w) <= 25
        ]

        # Count frequency
        word_counts = Counter(filtered)

        # Return top N tags
        tags = [word for word, count in word_counts.most_common(max_tags)]

        return tags

    def get_status(self) -> str:
        """Get OCR engine status message."""
        if not TESSERACT_AVAILABLE:
            return "❌ pytesseract not installed"
        if not self.is_available:
            return "❌ Tesseract OCR not found"
        if self.tesseract_path:
            return f"✅ Tesseract: {self.tesseract_path}"
        return "✅ Tesseract found in PATH"
