@echo off
setlocal EnableDelayedExpansion

:: =====================================================
:: YT-DLP Downloader Setup Script for Windows
:: =====================================================
:: Skips FFmpeg and virtual environment. Runs natively.
:: =====================================================

echo Starting setup for YT-DLP Downloader...
echo.

:: Variables
set "PYTHON_VERSION=3.11"

:: === Step 1: Check and Install Python ===
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing Python %PYTHON_VERSION% via winget...
    start /wait winget install --id Python.Python.%PYTHON_VERSION% -e --source winget
    if %errorlevel% neq 0 (
        echo Failed to install Python. Download manually from https://python.org.
        pause
        exit /b 1
    )
    echo Refreshing environment...
    call refreshenv
) else (
    echo Python is already installed.
)

:: Ensure pip is up-to-date
echo Updating pip...
python -m pip install --upgrade pip

:: === Step 2: Install or Update yt-dlp ===
echo Checking yt-dlp...
pip show yt-dlp >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing yt-dlp...
    pip install yt-dlp
    if %errorlevel% neq 0 (
        echo Failed to install yt-dlp.
        pause
        exit /b 1
    )
) else (
    echo Updating yt-dlp...
    pip install --upgrade yt-dlp
)

:: === Step 3: Install Project Dependencies ===
echo Installing project dependencies from requirements.txt...
if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies. Check requirements.txt.
        pause
        exit /b 1
    )
) else (
    echo requirements.txt not found. Skipping dependency installation.
)

:: === Step 4: Run the Script ===
echo Running main.py...
python main.py
if %errorlevel% neq 0 (
    echo Error running main.py. Check script or dependencies.
    pause
    exit /b 1
)

echo.
echo Execution complete! Downloads should be in the current directory.
pause
endlocal
