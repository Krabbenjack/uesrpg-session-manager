@echo off
REM UESRPG Session Manager launcher for Windows
REM This script launches the application with Python

REM Check if Python is available
where python >nul 2>nul
if errorlevel 1 (
    echo Python not found in PATH.
    echo.
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

python app.py
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
