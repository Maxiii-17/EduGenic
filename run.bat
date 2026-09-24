@echo off
cd /d "%~dp0"
echo ===============================
echo  Starting EduGenie...
echo  Opening http://127.0.0.1:8000
echo  Close this window to stop it.
echo ===============================
start "" /min cmd /c "timeout /t 6 /nobreak >nul & start http://127.0.0.1:8000"
python -m uvicorn main:app --port 8000
pause
