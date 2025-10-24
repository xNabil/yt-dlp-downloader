@echo off
setlocal EnableExtensions EnableDelayedExpansion
title YT-DLP Downloader Setup (Python + aria2 + FFmpeg)

echo ===============================
echo YT-DLP Downloader Setup
echo ===============================
echo.

:: Ensure winget exists
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo winget not found. Please install "App Installer" from Microsoft Store, then re-run this script.
    pause
    exit /b 1
)

:: Configuration
set "PYTHON_VERSION=3.11"
set "PYTHON_ID=Python.Python.%PYTHON_VERSION%"
set "PY_CMD=python"

:: Step 1: Check and install Python
echo Checking for Python...
%PY_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing Python %PYTHON_VERSION% via winget...
    call :WingetInstall "%PYTHON_ID%"
    if %errorlevel% neq 0 (
        echo Failed to install Python %PYTHON_VERSION%. Install manually and retry.
        pause
        exit /b 1
    )
) else (
    echo Python is already installed.
)

:: Ensure pip is up-to-date
echo Updating pip...
%PY_CMD% -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo pip upgrade failed. Continuing...
)

:: Step 2: Install or update yt-dlp
echo Installing/Updating yt-dlp...
%PY_CMD% -m pip install -U yt-dlp
if %errorlevel% neq 0 (
    echo Failed to install/update yt-dlp.
    pause
    exit /b 1
)

:: Step 3: Install project dependencies
if exist requirements.txt (
    echo Installing project dependencies from requirements.txt...
    %PY_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies from requirements.txt.
        pause
        exit /b 1
    )
) else (
    echo requirements.txt not found. Skipping dependency installation.
)

:: Step 4: Install aria2 and FFmpeg
echo ===============================
echo Installing aria2 and FFmpeg...
echo ===============================
call :WingetInstall "aria2.aria2"
if %errorlevel% neq 0 (
    echo aria2 installation failed.
) else (
    echo aria2 installed successfully.
)

call :WingetInstall "Gyan.FFmpeg"
if %errorlevel% neq 0 (
    echo FFmpeg installation failed.
) else (
    echo FFmpeg installed successfully.
)

:: Confirm installations
echo ===============================
echo Verifying installations...
echo ===============================
where aria2c >nul 2>nul
if %errorlevel% equ 0 (
    echo aria2c found in PATH.
) else (
    echo aria2c not found in PATH.
)

where ffmpeg >nul 2>nul
if %errorlevel% equ 0 (
    echo ffmpeg found in PATH.
) else (
    echo ffmpeg not found in PATH.
)

:: Step 5: Create .env from template (no overwrite)
echo ===============================
echo Preparing environment file...
echo ===============================
if exist ".env-example" (
    if not exist ".env" (
        copy /Y ".env-example" ".env" >nul
        if %errorlevel% neq 0 (
            echo Failed to copy .env-example to .env.
            pause
            exit /b 1
        ) else (
            echo Created .env from .env-example.
        )
    ) else (
        echo .env already exists. Skipping copy to preserve your settings.
    )
) else (
    echo .env-example not found. Skipping.
)

:: Step 6: Run main.py if present
if exist main.py (
    echo Running main.py...
    %PY_CMD% main.py
    if %errorlevel% neq 0 (
        echo Error running main.py. Check the script or dependencies.
        pause
        exit /b 1
    )
) else (
    echo main.py not found in the current directory. Skipping execution.
)

echo.
echo Execution complete! Downloads should be in the current directory if your script is configured that way.
pause
exit /b 0

:: Helper: silent winget installer with EULA acceptance and no interactivity
:WingetInstall
set "PKG=%~1"
echo Installing %PKG% via winget...
start /wait "" cmd /c winget install -e --id %PKG% --accept-package-agreements --accept-source-agreements --disable-interactivity --silent
exit /b %errorlevel%
