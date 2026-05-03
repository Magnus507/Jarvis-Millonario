@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8765/'"
python -m uvicorn server.dashboard:app --host 127.0.0.1 --port 8765
