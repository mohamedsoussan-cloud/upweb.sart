@echo off
setlocal
cd /d "%~dp0"
echo ================================================
echo The Printing Yassine - Client Windows distant
echo ================================================
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv || python -m venv .venv
  if errorlevel 1 goto erreur
)
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install pyinstaller
if not exist server_url.json copy server_url.json.example server_url.json
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --onedir --name "The Printing Yassine" --icon "icon.ico" desktop.py
if errorlevel 1 goto erreur
copy /Y server_url.json "dist\The Printing Yassine\server_url.json" >nul
echo.
echo Terminé. Distribuez tout le dossier dist\The Printing Yassine.
echo IMPORTANT : modifiez server_url.json avant la compilation si besoin.
pause
exit /b 0
:erreur
echo Une erreur est survenue. Vérifiez Python et la connexion Internet.
pause
exit /b 1
