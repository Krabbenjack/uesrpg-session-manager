@echo off
REM UESRPG Session Manager launcher for Windows
REM This script launches the application with Python

python app.py
if errorlevel 1 (
    echo.
    echo Failed to start the application.
    echo Make sure Python is installed and in your PATH.
    pause
)
