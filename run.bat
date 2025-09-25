@echo off
setlocal

:: =====================================================
:: Run YT-DLP Downloader Script
:: =====================================================
:: Runs main.py for https://github.com/xNabil/yt-dlp-downloader
:: Assumes setup.bat has been run to install dependencies
:: =====================================================

echo Starting YT-DLP Downloader...
echo.
:: Run the script
python main.py
if %errorlevel% neq 0 (
    echo Error running main.py. Ensure setup.bat was run and check dependencies.
    pause
    exit /b 1
)

echo.
echo Script execution complete! Downloads should be in the current directory.
pause
endlocal
