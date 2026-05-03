@echo off
cd /d "%~dp0"
start "MARK II ORB" /D "%~dp0" ".venv\Scripts\python.exe" -m uvicorn server.dashboard:app --host 127.0.0.1 --port 8765
powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 3; Start-Process 'http://127.0.0.1:8765/'"
call .venv\Scripts\activate.bat
python main.py
