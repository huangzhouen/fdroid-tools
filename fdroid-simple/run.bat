@echo off
chcp 65001 >nul
echo ============================================
echo    F-Droid Simple Repository
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not found. Install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python installed
echo.

if not exist "apps" mkdir apps
if not exist "repo" mkdir repo

echo [OK] Directories created
echo.

echo Starting server...
echo.

python server.py

pause