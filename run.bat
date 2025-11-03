@echo off
echo ============================================
echo    FOCUS OS - Starting Dashboard
echo ============================================
echo.
cd /d "%~dp0"
python src\ui\dashboard.py
pause