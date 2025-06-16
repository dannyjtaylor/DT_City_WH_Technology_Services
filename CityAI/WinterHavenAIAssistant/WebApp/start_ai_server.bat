@echo off
cd /d "%~dp0"
start "AI Server" cmd /k "uvicorn main:app --reload"
echo Waiting for server to start...
:loop
timeout /t 1 >nul
curl --silent http://127.0.0.1:8000 >nul
if errorlevel 1 goto loop
start "" http://127.0.0.1:8000
exit
