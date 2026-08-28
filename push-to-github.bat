@echo off
echo ========================================
echo    Git Push Script - Admin Required
echo ========================================
echo.
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [Error] Run as Administrator!
    pause
    exit /b 1
)
set REPO_DIR=D:\Administrator\Documents\codex
set REMOTE_URL=https://github.com/huangzhouen/fdroid-tools.git
echo [1/4] Enter repo directory...
cd /d ""%REPO_DIR%""
if not exist "".git"" (
    echo [Error] .git not found
    pause
    exit /b 1
)
echo [OK] Repository found
echo.
echo [2/4] Add remote...
git remote add origin %REMOTE_URL% 2>nul
echo [OK] Remote added
echo.
echo [3/4] Set branch name...
git branch -M main
echo [OK] Branch set to main
echo.
echo [4/4] Pushing to GitHub...
echo Username: huangzhouen
echo Password: Your GitHub Personal Access Token
echo.
git push -u origin main
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    SUCCESS!
    echo ========================================
    echo Visit: https://github.com/huangzhouen/fdroid-tools
) else (
    echo [Error] Push failed
)
pause