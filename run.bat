@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Installation Python requise. Lancez INSTALL.bat d'abord.
  pause
  exit /b 1
)
start "The Printing Yassine" /min "%~dp0.venv\Scripts\python.exe" "%~dp0desktop.py"
