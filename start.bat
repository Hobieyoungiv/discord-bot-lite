@echo off
cd /d "%~dp0"
where python >nul 2>nul || (echo Python is not installed. See README.md, step 1. & pause & exit /b 1)
if not exist .venv (
  echo First run: setting up, this takes about a minute...
  python -m venv .venv || (pause & exit /b 1)
  .venv\Scripts\python -m pip install --upgrade pip >nul
  .venv\Scripts\python -m pip install -r requirements.txt || (pause & exit /b 1)
)
if not exist .env (echo No .env file yet. Rename .env.example to .env and paste your token. See README.md, step 3. & pause & exit /b 1)
.venv\Scripts\python bot.py
pause
