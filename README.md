<![CDATA[<div align="center">

# 🖥️ ScreenZen — Screenshot Super-Organizer

**Stop drowning in screenshots. Start finding them instantly.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tesseract](https://img.shields.io/badge/Tesseract-OCR-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

</div>

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Key Features](#-key-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Building EXE](#-building-exe)
- [Project Structure](#-project-structure)
- [Future Roadmap](#-future-roadmap)
- [License](#-license)

---

## 😤 The Problem

Your desktop is buried under **1000+ screenshots** and you can never find *"that one image"* when you need it. Filenames like `Screenshot_2026-04-08_123456.png` tell you nothing. Scrolling through folders is a nightmare.

## ✨ The Solution

**ScreenZen** is a lightweight Python desktop app that lets you drag-and-drop your screenshots, automatically extracts text from them using OCR, organizes them by date and tags, and gives you **instant full-text search** across all your images.

> 🔍 Search YOUR screenshots by their **content**, not just filenames.

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| 📂 **Drag & Drop Upload** | Import screenshots via file dialog or drag-and-drop |
| 🔤 **OCR Text Extraction** | Powered by Tesseract — extracts all visible text from images |
| 🏷️ **Smart Tagging** | Auto-generated keyword tags from OCR results |
| 📅 **Date Grouping** | Screenshots organized by capture/import date |
| 🔍 **Full-Text Search** | Search across ALL extracted text instantly |
| 🖼️ **Gallery View** | Beautiful grid gallery with image previews |
| 📦 **Export ZIP** | Select and export screenshots as a zip archive |
| 🌙 **Dark Theme** | Modern, eye-friendly dark UI built with CustomTkinter |
| 💾 **Local SQLite DB** | All data stored locally — no cloud, no privacy concerns |
| 📊 **Dashboard Stats** | Total images, tags, and storage usage at a glance |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.9+ |
| **GUI Framework** | CustomTkinter (modern tkinter wrapper) |
| **OCR Engine** | Tesseract OCR via `pytesseract` |
| **Image Processing** | Pillow (PIL) |
| **Database** | SQLite3 (built-in) |
| **Packaging** | PyInstaller (for .exe conversion) |

---

## 📦 Installation

### Prerequisites

1. **Python 3.9+** — [Download here](https://www.python.org/downloads/)
2. **Tesseract OCR** — [Download here](https://github.com/UB-Mannheim/tesseract/wiki)
   - During installation, note the install path (default: `C:\Program Files\Tesseract-OCR`)
   - Add Tesseract to your system PATH, or the app will auto-detect common paths

### Setup

The easiest way to set up ScreenZen is using the automated scripts:

1. **Run `setup.bat`** — This will automatically create a virtual environment, install all dependencies, and set up your data directories.

Alternatively, you can set it up manually:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/SCREENZEN.git
cd SCREENZEN

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Windows (Command Prompt):
venv\Scripts\activate
# Windows (Git Bash / Bash):
source venv/Scripts/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the App

To launch ScreenZen:
- **Option A (Recommended):** Just double-click `run.bat`. This automatically uses the virtual environment.
- **Option B (Terminal):** Activate the `venv` and run `python main.py`.

### 🛠️ IDE Configuration (VS Code / PyCharm)

If you see "Module not found" or "Import error" in your IDE:
1. **VS Code:** Click on the Python version in the bottom-right status bar (or press `Ctrl+Shift+P` and type "Python: Select Interpreter").
2. Choose the interpreter located at `.\venv\Scripts\python.exe`.
3. This will resolve all import errors and enable full IntelliSense.

---

## 🎯 Usage

1. **Launch** the application with `python main.py`
2. **Import Screenshots** — Click "Add Screenshots" or use the drag-drop zone
3. **Wait for OCR** — Text extraction runs automatically in the background
4. **Search** — Type any keyword in the search bar to find matching screenshots
5. **Browse** — Use the gallery view, filter by date or tags
6. **Export** — Select images and click "Export ZIP" to bundle them

---

## 🏗️ Building EXE

Convert ScreenZen into a standalone Windows executable:

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Build the executable
pyinstaller --onefile --windowed --name ScreenZen --icon=assets/icon.ico main.py

# 3. Find your exe
# Output: dist/ScreenZen.exe
```

> **Note:** Make sure Tesseract OCR is installed on the target machine, or bundle it with the exe using `--add-data`.

### Bundling Tesseract with the EXE

```bash
pyinstaller --onefile --windowed --name ScreenZen --icon=assets/icon.ico \
  --add-data "C:\Program Files\Tesseract-OCR;Tesseract-OCR" \
  main.py
```

---

## 📁 Project Structure

```
SCREENZEN/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── assets/
│   └── icon.ico            # App icon
├── screenzen/
│   ├── __init__.py         # Package init
│   ├── app.py              # Main application window
│   ├── database.py         # SQLite database manager
│   ├── ocr_engine.py       # Tesseract OCR wrapper
│   ├── image_manager.py    # Image import/processing/export
│   ├── search_engine.py    # Full-text search logic
│   └── widgets/
│       ├── __init__.py     # Widgets package init
│       ├── gallery.py      # Gallery grid view widget
│       ├── sidebar.py      # Sidebar with tags/dates/stats
│       ├── search_bar.py   # Search bar widget
│       ├── image_card.py   # Individual image card widget
│       └── drop_zone.py    # Drag & drop upload zone
├── data/                   # Runtime data (auto-created)
│   ├── screenzen.db        # SQLite database
│   └── thumbnails/         # Cached image thumbnails
└── tests/
    └── test_ocr.py         # Basic OCR tests
```

---

## 🗺️ Future Roadmap

- [ ] **Auto-Capture** — Monitor clipboard/desktop for new screenshots
- [ ] **Annotation Tools** — Draw, highlight, and annotate screenshots
- [ ] **Cloud Sync** — Optional cloud storage with team sharing
- [ ] **Folder Watch** — Auto-import from watched directories
- [ ] **AI Tagging** — Smart categorization using ML models
- [ ] **Multi-language OCR** — Support for non-English text extraction
- [ ] **Batch Operations** — Bulk tag, delete, or export
- [ ] **Keyboard Shortcuts** — Power-user productivity features

---

## 💰 Monetization Ideas

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | Local storage, unlimited screenshots, full OCR |
| **Pro** | $2/mo | Cloud backup, team sharing, priority support |
| **Enterprise** | Custom | API access, SSO, admin dashboard |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ by ScreenZen**

*Stop scrolling. Start searching.*

</div>
]]>
