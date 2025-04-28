@echo off
mkdir reachable
mkdir not_reachable
call python -m venv venv
call activate_environment.bat
REM call pip install -r requirements.txt
if not exist settings.ini (
    copy settings_example.ini settings.ini
)
pause
