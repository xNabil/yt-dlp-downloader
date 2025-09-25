# YouTube Downloader

A command-line tool to download YouTube videos or audio using `yt-dlp`, with support for playlists, various quality options, and advanced settings like subtitles and metadata embedding.

## Features
- Download YouTube videos in MP4 format with selectable quality (360p to 4K).
- Download audio in MP3 format with selectable bitrates (128kbps to 320kbps).
- Advanced mode for custom `yt-dlp` format strings, subtitles, thumbnails, and metadata.
- Progress bar with download speed and ETA using `tqdm`.
- Colored terminal output for better user experience.
- Support for downloading entire playlists.
- Configuration saved in `~/.yt_dlp_config.json` for persistent settings.

## Prerequisites
- **Python 3.8+**: Ensure Python is installed.
- **FFmpeg**: Required for video/audio processing. Install it and add it to your system PATH:
  - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) or use a package manager like `choco install ffmpeg`.
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt-get install ffmpeg` (Ubuntu/Debian) or equivalent for your distribution.
- **Git**: For cloning the repository (optional).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/YouTube-Downloader.git
   cd YouTube-Downloader
