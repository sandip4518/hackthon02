@echo off
title ScreenZen Setup
color 0A

echo ============================================
echo    ScreenZen - Screenshot Super-Organizer
echo    Automated Setup Script
echo ============================================
echo.

:: Step 1: Check Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo [OK] Python found.
echo.

:: Step 2: Check Tesseract (using goto to avoid parentheses-in-path issues)
echo [2/6] Checking Tesseract OCR...
set TESSERACT_FOUND=0

tesseract --version >nul 2>&1
if %errorlevel% equ 0 set TESSERACT_FOUND=1
if %TESSERACT_FOUND% equ 1 goto :tess_ok

set "TESS_PATH1=C:\Program Files\Tesseract-OCR\tesseract.exe"
if exist "%TESS_PATH1%" set TESSERACT_FOUND=1
if %TESSERACT_FOUND% equ 1 goto :tess_ok

set "TESS_PATH2=C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
if exist "%TESS_PATH2%" set TESSERACT_FOUND=1
if %TESSERACT_FOUND% equ 1 goto :tess_ok

:: Tesseract not found
echo [WARNING] Tesseract OCR not found!
echo The app will work but OCR features will be disabled.
echo Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
echo.
set /p CONTINUE="Continue without Tesseract? (Y/N): "
if /i not "%CONTINUE%"=="Y" goto :tess_cancel
goto :tess_done

:tess_cancel
echo Setup cancelled. Install Tesseract and run again.
pause
exit /b 1

:tess_ok
echo [OK] Tesseract OCR found.

:tess_done
echo.

:: Step 3: Clean old Node.js files (from previous version)
echo [3/6] Cleaning legacy files...
if exist "node_modules" rmdir /s /q node_modules
if exist "package.json" del /q package.json
if exist "package-lock.json" del /q package-lock.json
if exist "postcss.config.js" del /q postcss.config.js
if exist "postcss.config.mjs" del /q postcss.config.mjs
if exist "tailwind.config.ts" del /q tailwind.config.ts
if exist "tsconfig.json" del /q tsconfig.json
if exist "next-env.d.ts" del /q next-env.d.ts
if exist "next.config.mjs" del /q next.config.mjs
if exist "next.config.js" del /q next.config.js
if exist "app" rmdir /s /q app
if exist "components" rmdir /s /q components
if exist "lib" rmdir /s /q lib
echo [OK] Legacy files cleaned.
echo.

:: Step 4: Create virtual environment
echo [4/6] Creating virtual environment...
if exist "venv" rmdir /s /q venv
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment created.
echo.

:: Step 5: Install dependencies
echo [5/6] Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo.
echo [OK] All dependencies installed.
echo.

:: Step 6: Create data directories
echo [6/6] Creating data directories...
if not exist "data" mkdir data
if not exist "data\images" mkdir data\images
if not exist "data\thumbnails" mkdir data\thumbnails
echo [OK] Data directories ready.
echo.

:: Run tests
echo ============================================
echo Running quick tests...
echo ============================================
python -m unittest tests.test_ocr -v
echo.

:: Done
echo ============================================
echo.
echo    [SUCCESS] ScreenZen setup complete!
echo.
echo    To run the app:
echo      1. Open terminal in this folder
echo      2. Run: venv\Scripts\activate
echo      3. Run: python main.py
echo.
echo    Or just run: run.bat
echo.
echo ============================================
echo.

:: Ask to launch
set /p LAUNCH="Launch ScreenZen now? (Y/N): "
if /i "%LAUNCH%"=="Y" (
    echo Starting ScreenZen...
    python main.py
)

pause
