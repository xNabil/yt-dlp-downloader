@echo off
setlocal EnableDelayedExpansion

:: =====================================================
:: YT-DLP Downloader Setup Script for Windows
:: =====================================================
:: Installs Python, yt-dlp, FFmpeg, project dependencies, and runs main.py
:: Requirements: Internet connection, 7-Zip installed for FFmpeg extraction
:: Target: https://github.com/xNabil/yt-dlp-downloader
:: =====================================================

echo Starting setup for YT-DLP Downloader...
echo.

:: Variables
set "FFMPEG_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z"
set "FFMPEG_DIR=C:\ffmpeg"
set "PYTHON_VERSION=3.11"

:: === Step 1: Check and Install Python ===
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing Python %PYTHON_VERSION% via winget...
    winget install Python.Python.%PYTHON_VERSION%
    if %errorlevel% neq 0 (
        echo Failed to install Python. Download manually from https://python.org.
        pause
        exit /b 1
    )
    echo Refreshing environment to include Python...
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
) else (
    echo Updating yt-dlp to latest version...
    pip install --upgrade yt-dlp
)
if %errorlevel% neq 0 (
    echo Failed to install/update yt-dlp. Check your internet or pip.
    pause
    exit /b 1
)

:: === Step 3: Install FFmpeg ===
echo Checking for FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing FFmpeg (essentials build, ~31MB)...
    echo Target folder: %FFMPEG_DIR%

    :: Create FFmpeg folder
    if not exist "%FFMPEG_DIR%" mkdir "%FFMPEG_DIR%"

    :: Download FFmpeg archive
    echo Downloading FFmpeg...
    curl -L %FFMPEG_URL% -o "%FFMPEG_DIR%\ffmpeg.7z"
    if %errorlevel% neq 0 (
        echo Failed to download FFmpeg. Check your internet or URL.
        pause
        exit /b 1
    )

    :: Check for 7-Zip
    7z >nul 2>&1
    if %errorlevel% neq 0 (
        echo 7-Zip not found. Installing via winget...
        winget install 7zip.7zip
        if %errorlevel% neq 0 (
            echo Failed to install 7-Zip. Download manually from https://www.7-zip.org.
            pause
            exit /b 1
        )
        call refreshenv
    )

    :: Extract FFmpeg
    echo Extracting FFmpeg...
    7z x "%FFMPEG_DIR%\ffmpeg.7z" -o"%FFMPEG_DIR%" -y
    if %errorlevel% neq 0 (
        echo Failed to extract FFmpeg. Ensure 7-Zip is installed.
        pause
        exit /b 1
    )

    :: Find extracted folder
    for /d %%i in ("%FFMPEG_DIR%\ffmpeg-*-essentials") do set "EXTRACTED=%%i"

    :: Move bin folder
    if exist "%EXTRACTED%\bin" (
        echo Organizing FFmpeg files...
        if not exist "%FFMPEG_DIR%\bin" mkdir "%FFMPEG_DIR%\bin"
        xcopy "%EXTRACTED%\bin\*" "%FFMPEG_DIR%\bin\" /E /I /Y
    )

    :: Add FFmpeg to system PATH
    echo Adding FFmpeg to system PATH...
    setx /M PATH "%PATH%;%FFMPEG_DIR%\bin"
    if %errorlevel% neq 0 (
        echo Failed to update PATH. Add %FFMPEG_DIR%\bin manually to PATH.
    )

    :: Cleanup
    del "%FFMPEG_DIR%\ffmpeg.7z"
    if exist "%EXTRACTED%" rmdir /S /Q "%EXTRACTED%"
    echo FFmpeg installed successfully!
) else (
    echo FFmpeg is already installed.
)

:: Test FFmpeg
echo Verifying FFmpeg...
%FFMPEG_DIR%\bin\ffmpeg.exe -version >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg verification failed. Ensure %FFMPEG_DIR%\bin is in PATH.
    pause
    exit /b 1
)

:: === Step 4: Create and Activate Virtual Environment ===
echo Setting up virtual environment...
if not exist venv (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment. Continuing without...
    )
)
call venv\Scripts\activate.bat

:: === Step 5: Install Project Dependencies ===
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

:: === Step 6: Run the Script ===
echo Setup complete! Running main.py...
python main.py
if %errorlevel% neq 0 (
    echo Error running main.py. Check script or dependencies.
    pause
    exit /b 1
)

echo.
echo Execution complete! Downloads should be in the current directory.
echo Restart your terminal or PC if FFmpeg or Python commands are not recognized.
pause
endlocal
