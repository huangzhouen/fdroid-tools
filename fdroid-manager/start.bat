@echo off
chcp 65001 >nul
echo ============================================
echo    F-Droid Manager
echo ============================================
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not found
    pause
    exit /b 1
)
echo Starting GUI...
python "%~dp0app.py"
pause
