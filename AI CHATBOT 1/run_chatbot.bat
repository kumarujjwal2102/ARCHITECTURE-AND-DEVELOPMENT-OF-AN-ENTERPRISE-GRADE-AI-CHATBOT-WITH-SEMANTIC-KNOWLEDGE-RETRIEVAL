@echo off
setlocal
echo ==========================================
echo Starting Enterprise AI Chatbot Backend...
echo ==========================================

cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment (.venv) not found!
    echo Please run 'python -m venv .venv' and 'pip install -r backend/requirements.txt'
    pause
    exit /b
)

cd backend
..\\.venv\Scripts\python.exe main.py
pause

