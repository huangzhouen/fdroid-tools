@echo off
echo ========================================
echo    Pushing to GitHub
echo ========================================
echo.

cd /d "D:\Administrator\Documents\codex"

echo [1/4] Adding remote...
git remote add origin https://github.com/huangzhouen/fdroid-tools.git 2>nul
echo [OK] Remote added

echo.
echo [2/4] Setting branch name...
git branch -M main
echo [OK] Branch set to main

echo.
echo [3/4] Checking status...
git status
echo.

echo [4/4] Pushing to GitHub...
echo Username: huangzhouen
echo Password: Your GitHub Token
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    SUCCESS!
    echo ========================================
    echo Repository: https://github.com/huangzhouen/fdroid-tools
) else (
    echo.
    echo [Error] Push failed
    echo Check your GitHub credentials
)

pause