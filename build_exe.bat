@echo off
title ScreenZen - Build EXE
color 0E

echo ============================================
echo    ScreenZen - Building EXE
echo ============================================
echo.

cd /d "%~dp0"

:: Activate venv
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found! Run setup.bat first.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat

:: Install PyInstaller if not present
echo [1/3] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)
echo [OK] PyInstaller ready.
echo.

:: Clean previous builds
echo [2/3] Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "ScreenZen.spec" del /q ScreenZen.spec
echo [OK] Clean.
echo.

:: Build
echo [3/3] Building ScreenZen.exe...
echo This may take a few minutes...
echo.

if exist "assets\icon.ico" (
    pyinstaller --onefile --windowed --name ScreenZen --icon=assets\icon.ico main.py
) else (
    pyinstaller --onefile --windowed --name ScreenZen main.py
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo.
echo    [SUCCESS] EXE built successfully!
echo    Location: dist\ScreenZen.exe
echo.
echo    NOTE: Tesseract OCR must be installed
echo    on the target machine for OCR to work.
echo.
echo ============================================

:: Open dist folder
explorer dist

pause
