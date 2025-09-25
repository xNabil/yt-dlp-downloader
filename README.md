# yt-dlp-downloader

A simple, interactive, and user-friendly Python script to download YouTube videos and playlists as videos (MP4), audios (MP3), or with advanced custom options. This project wraps the powerful [yt-dlp](https://github.com/yt-dlp/yt-dlp) tool into a clean terminal interface, so you don't need to remember or type long yt-dlp commands.

![yt-dlp-downloader screenshot](docs/screenshot.png) <!-- Add a screenshot to docs/screenshot.png if you have one -->

---

## Features

- **Download YouTube videos** as MP4, MP3, or with advanced custom options.
- **Interactive, menu-driven terminal UI** — no need to type long yt-dlp commands.
- **Batch downloads** for playlists or multiple videos.
- **Custom output formats, quality, and more.**
- **Easy to use:** Just run and follow the prompts.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions (Manual & Automated)](#setup-instructions-manual--automated)
  - [1. Install Python](#1-install-python)
  - [2. Install FFmpeg (and Add to PATH)](#2-install-ffmpeg-and-add-to-path)
  - [3. Install yt-dlp-downloader Dependencies](#3-install-yt-dlp-downloader-dependencies)
  - [4. Run the Script](#4-run-the-script)
  - [Automated Setup (Windows)](#automated-setup-windows)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Requirements

- **Windows** (Batch scripts provided; works on other OS with minor adjustments)
- **Python 3.7+**
- **FFmpeg** (for audio/video conversion, merging, etc.)
- **yt-dlp** (will be installed automatically)
- Internet access

---

## Setup Instructions (Manual & Automated)

### 1. Install Python

- Download and install Python 3.7 or newer from [python.org/downloads](https://www.python.org/downloads/).
- During installation, **check the box "Add Python to PATH"**.

### 2. Install FFmpeg (and Add to PATH)

**FFmpeg** is required for video/audio processing.

#### a. Download FFmpeg

- Go to [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- For Windows, click on "Windows" and choose a build (e.g., [gyan.dev builds](https://www.gyan.dev/ffmpeg/builds/)).
- Download the latest **release full build** as a ZIP file.

#### b. Extract and Add to PATH

1. Extract the ZIP file (e.g., to `C:\ffmpeg`).
2. Inside the extracted folder, locate the `bin` directory (e.g., `C:\ffmpeg\bin`).
3. **Add `C:\ffmpeg\bin` to your Windows PATH:**
   - Press `Win + S`, type "Environment Variables", and select "Edit the system environment variables".
   - Click "Environment Variables".
   - Under "System variables", select "Path" and click "Edit".
   - Click "New" and add the path to your FFmpeg `bin` folder (e.g., `C:\ffmpeg\bin`).
   - Click OK on all dialogs.

4. **Verify installation:**
   - Open a new terminal/command prompt and run:
     ```
     ffmpeg -version
     ```
   - If you see version info, you're set!

### 3. Install yt-dlp-downloader Dependencies

- Open a terminal/command prompt in the project folder.
- Run:
  ```
  pip install -r requirements.txt
  ```
  This will install `yt-dlp` and any other dependencies.

### 4. Run the Script

- **Windows:**
  - Double-click `run.bat` or run in terminal:
    ```
    python main.py
    ```

- **Linux/macOS:**
  - Run:
    ```
    python3 main.py
    ```

---

### Automated Setup (Windows)

- **setup.bat:**  
  Just double-click `setup.bat` to:
  - Automatically install Python dependencies
  - Download and install yt-dlp
  - Optionally help install FFmpeg (if scripted)
  - Prepare everything for you
  
  > **Note:** You may still need to manually install FFmpeg and add it to your PATH if not fully automated by the script.

- **run.bat:**  
  Double-click to launch the downloader with one click.

---

## Usage

1. **Launch the downloader:**  
   - Run `run.bat` or execute `python main.py`.
2. **Follow the on-screen prompts:**  
   - Enter the YouTube link(s), select output format (video/audio), quality, and other options.
3. **Wait for download and processing to complete.**
4. **Your files will be saved in the specified output directory.**

---

## File Descriptions

- **main.py** — The main Python script; entry point for the downloader.
- **requirements.txt** — Lists required Python packages (yt-dlp, etc).
- **setup.bat** — Automates initial setup: installs dependencies, may help with FFmpeg/yt-dlp setup.
- **run.bat** — Launches the downloader easily.
- **README.md** — This file.
- **docs/** — (Optional) Screenshots or documentation.

---

## Troubleshooting

- **FFmpeg not found error:**  
  Ensure FFmpeg is installed and the `bin` folder is in your PATH. Close and reopen your terminal after adding to PATH.

- **yt-dlp not found:**  
  Make sure `pip install -r requirements.txt` ran successfully.

- **Permission errors:**  
  Try running your terminal as administrator.

- **Still stuck?**  
  Open an issue on [GitHub Issues](https://github.com/xNabil/yt-dlp-downloader/issues).

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
