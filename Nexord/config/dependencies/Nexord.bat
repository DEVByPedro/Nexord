@echo off

set "APP_DIR=%~dp0"
set "PARENT_DIR=%APP_DIR%..\..\"

if not exist "%PARENT_DIR%venv\Scripts\python.exe" (
    python.exe -m venv %PARENT_DIR%venv
)

call "%PARENT_DIR%venv\Scripts\activate.bat"

python.exe %PARENT_DIR%main.py

pause