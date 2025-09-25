# yt-dlp-downloader
---

## Features

- **Download YouTube videos or entire playlists** as MP4 (video) or MP3 (audio)
- **Interactive menus** for quality selection (360p, 720p, 1080p, etc.), audio bitrate, and advanced yt-dlp formats
- **Progress bars** (with [tqdm](https://pypi.org/project/tqdm/)) for each download, including playlists
- **Colored terminal output** using [colorama](https://pypi.org/project/colorama/)
- **Downloads are saved in your `~/Downloads/YT-DLP/Videos` or `~/Downloads/YT-DLP/Audios` directories**
- **No need to remember yt-dlp command-line arguments**
- **FFmpeg check**: Warns you if ffmpeg is not installed
- **Automatic config file**: Remembers your last used options (in `~/.yt_dlp_config.json`)
- **Safe and clean filenames** for downloaded files
- **Extensible**: Easy to add more features or options

---

## Requirements

- **Python 3.7+**
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (`pip install yt-dlp`)
- [colorama](https://pypi.org/project/colorama/) (`pip install colorama`)
- [tqdm](https://pypi.org/project/tqdm/) (`pip install tqdm`)
- **ffmpeg** installed and available in your system PATH (for audio extraction and merging)

Install dependencies with:

```bash
pip install yt-dlp colorama tqdm
```

On Linux/macOS, you can install `ffmpeg` via your package manager. On Windows, download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your PATH.

---

## Usage

1. **Clone this repository or download `main.py`.**
2. **Run the script:**

    ```bash
    python3 main.py
    ```

3. **Follow the interactive prompts:**
    - Paste one or more YouTube video/playlist links.
    - Choose download type: Video (MP4), Audio (MP3), or Advanced (custom yt-dlp format).
    - Select video or audio quality, or set advanced options.
    - Approve the pre-download summary.
    - Watch your downloads with real-time progress bars!

---

## Example Session

```
Enter YouTube video or playlist links (separated by space):
➤ https://www.youtube.com/watch?v=dQw4w9WgXcQ

Choose download type:
1. Video (MP4)
2. Audio (MP3 / other)
3. Advanced (custom format & options)
➤ Enter choice (1-3, default: 1):

Available video qualities:
1. Best Quality available
2. 360p
3. 480p
4. 720p (SD)
5. 1080p (FHD)
...
➤ Select quality (1-7, default: best):

========================
--- Download Info ---
========================
Title: Rick Astley - Never Gonna Give You Up ...
Uploader: RickAstleyVEVO
Duration: 00:03:32
Chosen format: 720p
Size: 12.34 MiB
Destination: /home/user/Downloads/YT-DLP/Videos/Rick Astley - Never Gonna Give You Up (720p).mp4
➤ Proceed? (y/n):
```

---

## Why use this script?

- **No need to memorize yt-dlp commands!**
- Handles playlists, quality selection, and file naming for you.
- Clean, color-coded output and real-time progress.
- One file, no external GUIs, just Python and a terminal.

---

## Configuration

- The script stores your last used settings (quality, type, etc.) in `~/.yt_dlp_config.json`.
- Downloaded files are saved in `~/Downloads/YT-DLP/Videos` (videos) or `~/Downloads/YT-DLP/Audios` (audio) by default.

---

## Customization

You can easily modify `main.py` to:
- Change default download folders
- Add support for other sites supported by yt-dlp
- Add post-processing or notifications

---

## Troubleshooting

- **FFmpeg not found?**  
  Make sure `ffmpeg` is installed and available in your system PATH.

- **Corrupted config file?**  
  The script will reset options to default if `~/.yt_dlp_config.json` is invalid.

- **Issues with certain links?**  
  Some videos may be region-locked or age-restricted; yt-dlp may need extra options.

---

## License

This project is licensed under the MIT License.

---

## Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the actual downloading
- [colorama](https://pypi.org/project/colorama/) for colored output
- [tqdm](https://pypi.org/project/tqdm/) for pretty progress bars

---

## Contribution

Pull requests are welcome for bugfixes, features, and improvements!

---

**Happy downloading!**
