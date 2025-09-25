#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path
import subprocess
import yt_dlp
from colorama import init, Fore, Style
import shutil
from tqdm import tqdm
import time

# Initialize colorama for colored terminal output
init(autoreset=True)

# Define directories
HOME = Path.home()
VIDEO_DIR = HOME / "Downloads" / "YT-DLP" / "Videos"
AUDIO_DIR = HOME / "Downloads" / "YT-DLP" / "Audios"
CONFIG_FILE = HOME / ".yt_dlp_config.json"

# Ensure directories exist
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Check if ffmpeg is available
def check_ffmpeg():
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        print(f"{Fore.RED}Error: FFmpeg is not installed or not found in PATH. Please install FFmpeg and add it to your system PATH.{Style.RESET_ALL}")
        return False
    return True

# Load default settings
def load_config():
    default_config = {
        "download_type": "1",
        "video_quality": "best",
        "audio_quality": "320",
        "advanced_format": "bestvideo+bestaudio/best",
        "subtitles": False,
        "thumbnails": False,
        "metadata": False
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: Corrupted config file. Using default settings.{Style.RESET_ALL}")
    return default_config

# Clean filename to be filesystem-safe
def clean_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title).strip()[:200]  # Basic cleaning, consider pathvalidate for more robustness

# Get video info using yt-dlp
def get_video_info(url):
    with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except yt_dlp.DownloadError as e:
            print(f"{Fore.RED}Error: Invalid link {url} - {str(e)}{Style.RESET_ALL}")
            return None

# Get user input for links
def get_links():
    print(f"{Fore.GREEN}Enter YouTube video or playlist links (separated by space):{Style.RESET_ALL}")
    links = input(f"{Fore.CYAN}➤ {Style.RESET_ALL}").strip().split()
    valid_links = [link for link in links if re.match(r'https?://.*', link)]
    if not valid_links:
        print(f"{Fore.RED}No valid URLs provided. Exiting.{Style.RESET_ALL}")
        return []
    return valid_links

# Display download type menu
def choose_download_type(config):
    print(f"{Fore.BLUE}Choose download type:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Video (MP4){Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. Audio (MP3 / other){Style.RESET_ALL}")
    print(f"{Fore.GREEN}3. Advanced (custom format & options){Style.RESET_ALL}")
    choice = input(f"{Fore.CYAN}➤ Enter choice (1-3, default: {config['download_type']}): {Style.RESET_ALL}").strip() or config['download_type']
    while choice not in ['1', '2', '3']:
        print(f"{Fore.RED}Invalid choice. Please select 1, 2, or 3.{Style.RESET_ALL}")
        choice = input(f"{Fore.CYAN}➤ Enter choice (1-3): {Style.RESET_ALL}").strip() or config['download_type']
    return choice

# Choose video quality
def choose_video_quality(config):
    qualities = ["best", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
    print(f"{Fore.BLUE}Available video qualities:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Best Quality available{Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. 360p{Style.RESET_ALL}")
    print(f"{Fore.GREEN}3. 480p{Style.RESET_ALL}")
    print(f"{Fore.GREEN}4. 720p (SD){Style.RESET_ALL}")
    print(f"{Fore.GREEN}5. 1080p (FHD){Style.RESET_ALL}")
    print(f"{Fore.GREEN}6. 1440p (QHD){Style.RESET_ALL}")
    print(f"{Fore.GREEN}7. 2160p (4K){Style.RESET_ALL}")
    choice = input(f"{Fore.CYAN}➤ Select quality (1-{len(qualities)}, default: {config['video_quality']}): {Style.RESET_ALL}").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(qualities):
        return qualities[int(choice) - 1]
    return config['video_quality']

# Choose audio quality
def choose_audio_quality(config):
    qualities = ["best", "128", "192", "256", "320"]
    print(f"{Fore.BLUE}Available audio qualities (MP3):{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Best Quality Available{Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. Standard Quality (128 kbps){Style.RESET_ALL}")
    print(f"{Fore.GREEN}3. High Quality (192 kbps){Style.RESET_ALL}")
    print(f"{Fore.GREEN}4. Very High Quality (256 kbps){Style.RESET_ALL}")
    print(f"{Fore.GREEN}5. Extreme Quality (320 kbps){Style.RESET_ALL}")
    choice = input(f"{Fore.CYAN}➤ Select quality (1-5, default: {config['audio_quality']} kbps): {Style.RESET_ALL}").strip()
    if choice.isdigit() and 1 <= int(choice) <= 5:
        return qualities[int(choice) - 1]
    return config['audio_quality']

# Advanced options
def choose_advanced_options(config):
    print(f"{Fore.BLUE}Advanced download options:{Style.RESET_ALL}")
    format_str = input(f"{Fore.CYAN}➤ Enter custom yt-dlp format (default: {config['advanced_format']}): {Style.RESET_ALL}").strip() or config['advanced_format']
    subtitles = input(f"{Fore.CYAN}➤ Download subtitles? (y/n, default: {'y' if config['subtitles'] else 'n'}): {Style.RESET_ALL}").strip().lower() == 'y'
    thumbnails = input(f"{Fore.CYAN}➤ Download thumbnails? (y/n, default: {'y' if config['thumbnails'] else 'n'}): {Style.RESET_ALL}").strip().lower() == 'y'
    metadata = input(f"{Fore.CYAN}➤ Embed metadata? (y/n, default: {'y' if config['metadata'] else 'n'}): {Style.RESET_ALL}").strip().lower() == 'y'
    return format_str, subtitles, thumbnails, metadata

# Format file size
def format_size(bytes_size):
    if not bytes_size:
        return "Unknown"
    mb_size = bytes_size / (1024 * 1024)
    return f"{mb_size:.2f} MiB"

# Display pre-download info
def show_pre_download_info(info, format_info, dest_path, quality):
    print(f"{Fore.YELLOW}{'='*24}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}--- Download Info ---{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*24}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Title: {info.get('title', 'Unknown')}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Uploader: {info.get('uploader', 'Unknown')}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Duration: {info.get('duration_string', 'Unknown')}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Chosen format: {format_info}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Size: {format_size(info.get('filesize') or info.get('filesize_approx'))}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Destination: {dest_path}{Style.RESET_ALL}")
    return input(f"{Fore.CYAN}➤ Proceed? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'

# Progress bar for downloads
def create_progress_bar(total_size_mb, title):
    if total_size_mb and total_size_mb > 0:
        # Use actual file size if available
        return tqdm(total=total_size_mb, desc=f"{Fore.GREEN}Downloading {title[:30]}{Style.RESET_ALL}", unit="MiB", bar_format="{l_bar}{bar}| {n:.1f}/{total:.1f} MiB [{elapsed}<{remaining}, {postfix}]")
    else:
        # Fallback to percentage-based progress bar
        return tqdm(total=100, desc=f"{Fore.GREEN}Downloading {title[:30]}{Style.RESET_ALL}", unit="%", bar_format="{l_bar}{bar}| {n:.1f}% [{elapsed}<{remaining}, {postfix}]")

# Download video
def download_video(url, quality, config):
    if not check_ffmpeg():
        return False
    
    # Determine if URL is a playlist
    with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': True}) as ydl:
        try:
            flat_info = ydl.extract_info(url, download=False)
            is_playlist = 'entries' in flat_info
        except yt_dlp.DownloadError as e:
            print(f"{Fore.RED}Error: Invalid link {url} - {str(e)}{Style.RESET_ALL}")
            return False
    
    format_str = "bestvideo+bestaudio/best" if quality == "best" else f"bv*[height<={quality[:-1]}]+ba/best"
    format_display = quality if quality != "best" else "best"
    
    if is_playlist:
        playlist_title = flat_info.get('title', 'Unknown Playlist')
        num_videos = len(flat_info['entries'])
        print(f"{Fore.BLUE}🎥 Playlist: {playlist_title}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📋 Number of videos: {num_videos}{Style.RESET_ALL}")
        if input(f"{Fore.CYAN}➤ Proceed with downloading playlist? (y/n): {Style.RESET_ALL}").strip().lower() != 'y':
            return False
        output_filename = "%(title)s (%(height)sp).%(ext)s"
        output_path = VIDEO_DIR / output_filename
        pbar = None
        video_count = 0
    else:
        # Single video: fetch info with specified format for accurate size
        ydl_opts_info = {
            'format': format_str,
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl_info:
            try:
                info = ydl_info.extract_info(url, download=False)
            except yt_dlp.DownloadError as e:
                print(f"{Fore.RED}Error fetching info for {url}: {str(e)}. Falling back to best available.{Style.RESET_ALL}")
                ydl_opts_info['format'] = 'bestvideo+bestaudio/best'
                with yt_dlp.YoutubeDL(ydl_opts_info) as ydl_info:
                    info = ydl_info.extract_info(url, download=False)
                format_str = 'bestvideo+bestaudio/best'
                format_display = "best"
        
        if not info:
            return False
        title = clean_filename(info['title'])
        height = info.get('height', 'best')
        quality_display = f"{height}p" if height and format_display == "best" else format_display
        output_filename = f"{title} ({quality_display}).%(ext)s"
        output_path = VIDEO_DIR / output_filename
        
        if not show_pre_download_info(info, quality_display, str(output_path), quality):
            return False
        total_size_mb = (info.get('filesize') or info.get('filesize_approx') or 0) / (1024 * 1024)
        pbar = create_progress_bar(total_size_mb, title)
        video_count = 0
    
    last_update = 0
    last_bytes = 0
    current_title = ""
    
    def progress_hook(d):
        nonlocal pbar, last_update, last_bytes, current_title, video_count
        current_time = time.time()
        if d['status'] == 'downloading':
            # Get current video title
            title = d.get('info_dict', {}).get('title', 'Unknown')
            total_size_mb = (d.get('info_dict', {}).get('filesize') or d.get('info_dict', {}).get('filesize_approx') or 0) / (1024 * 1024)
            if title != current_title:
                if pbar:
                    pbar.close()
                video_count += 1
                current_title = title
                desc = f"Video {video_count}/{num_videos}: {title[:30]}" if is_playlist else title[:30]
                pbar = create_progress_bar(total_size_mb, desc)
            
            # Update every 0.1 seconds
            if current_time - last_update >= 0.1:
                # Strip ANSI codes from _percent_str
                percent_str = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', d.get('_percent_str', '0%')).strip('%')
                try:
                    percent = float(percent_str)
                except ValueError:
                    percent = 0.0
                # Calculate downloaded size in MiB
                downloaded_bytes = d.get('downloaded_bytes', 0)
                downloaded_mb = downloaded_bytes / (1024 * 1024)
                # Calculate speed manually
                time_delta = current_time - last_update if last_update else 0.1
                speed_mb_s = (downloaded_bytes - last_bytes) / (1024 * 1024 * time_delta) if time_delta > 0 else 0.0
                last_bytes = downloaded_bytes
                last_update = current_time
                # Update progress bar
                if pbar and pbar.total > 0 and total_size_mb > 0:
                    pbar.n = downloaded_mb
                elif pbar:
                    pbar.n = percent
                # Update postfix with ETA and speed
                eta = d.get('eta', 'Unknown')
                eta_str = f"ETA {time.strftime('%M:%S', time.gmtime(eta))}" if eta != 'Unknown' else 'ETA Unknown'
                if pbar:
                    pbar.set_postfix_str(f"{eta_str}, {speed_mb_s:.2f}MiB/s")
                    pbar.refresh()
        elif d['status'] == 'finished':
            if pbar:
                if pbar.total > 0:
                    pbar.n = pbar.total
                else:
                    pbar.n = 100
                pbar.refresh()
                pbar.close()
                pbar = None
            print(f"{Fore.GREEN}✅ Download complete: {d.get('filename', 'Unknown')}{Style.RESET_ALL}")

    ydl_opts = {
        'format': format_str,
        'outtmpl': str(output_path),
        'merge_output_format': 'mp4',
        'nopostoverwrites': True,  # Prevent overwriting during post-processing
        'ffmpeg_location': None,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
        'paths': {'home': str(VIDEO_DIR), 'temp': str(VIDEO_DIR)}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except yt_dlp.DownloadError as e:
        if not is_playlist:
            print(f"{Fore.RED}Error downloading {url}: {str(e)}. Falling back to best available.{Style.RESET_ALL}")
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            ydl_opts['outtmpl'] = str(VIDEO_DIR / f"{title} ({info.get('height', 'best')}p).%(ext)s")
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                filename = VIDEO_DIR / f"{title} ({info.get('height', 'best')}p).mp4"
                print(f"{Fore.GREEN}✅ Download complete: {filename}{Style.RESET_ALL}")
                return True
            except yt_dlp.DownloadError as e:
                print(f"{Fore.RED}Failed to download {url}: {str(e)}{Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.RED}Error downloading playlist {url}: {str(e)}{Style.RESET_ALL}")
            return False

# Download audio
def download_audio(url, audio_quality, config):
    if not check_ffmpeg():
        return False
    
    # Check if URL is a playlist
    with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': True}) as ydl:
        try:
            flat_info = ydl.extract_info(url, download=False)
            is_playlist = 'entries' in flat_info
        except yt_dlp.DownloadError as e:
            print(f"{Fore.RED}Error: Invalid link {url} - {str(e)}{Style.RESET_ALL}")
            return False
    
    quality_display = f"{audio_quality}kbps" if audio_quality != "best" else "320kbps"
    
    if is_playlist:
        playlist_title = flat_info.get('title', 'Unknown Playlist')
        num_videos = len(flat_info['entries'])
        print(f"{Fore.BLUE}🎵 Playlist: {playlist_title}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📋 Number of videos: {num_videos}{Style.RESET_ALL}")
        if input(f"{Fore.CYAN}➤ Proceed with downloading playlist? (y/n): {Style.RESET_ALL}").strip().lower() != 'y':
            return False
        output_filename = f"%(title)s ({quality_display}).mp3"
        output_path = AUDIO_DIR / output_filename
        pbar = None
        video_count = 0
    else:
        # Single audio: get info and show pre-download info
        ydl_opts_info = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': audio_quality if audio_quality != 'best' else '320',
            }],
            'quiet': True,
            'no_warnings': True,
            'simulate': True
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
            except yt_dlp.DownloadError as e:
                print(f"{Fore.RED}Error: Invalid link {url} - {str(e)}{Style.RESET_ALL}")
                return False
        
        title = clean_filename(info['title'])
        output_path = AUDIO_DIR / f"{title} ({quality_display}).mp3"
        
        if not show_pre_download_info(info, f"mp3 ({quality_display})", str(output_path), audio_quality):
            return False
        total_size_mb = (info.get('filesize') or info.get('filesize_approx') or 0) / (1024 * 1024)
        pbar = create_progress_bar(total_size_mb, title)
        video_count = 0
    
    last_update = 0
    last_bytes = 0
    current_title = ""
    
    def progress_hook(d):
        nonlocal pbar, last_update, last_bytes, current_title, video_count
        current_time = time.time()
        if d['status'] == 'downloading':
            # Get current video title
            title = d.get('info_dict', {}).get('title', 'Unknown')
            total_size_mb = (d.get('info_dict', {}).get('filesize') or d.get('info_dict', {}).get('filesize_approx') or 0) / (1024 * 1024)
            if title != current_title:
                if pbar:
                    pbar.close()
                video_count += 1
                current_title = title
                desc = f"Audio {video_count}/{num_videos}: {title[:30]}" if is_playlist else title[:30]
                pbar = create_progress_bar(total_size_mb, desc)
            
            # Update every 0.1 seconds
            if current_time - last_update >= 0.1:
                # Strip ANSI codes from _percent_str
                percent_str = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', d.get('_percent_str', '0%')).strip('%')
                try:
                    percent = float(percent_str)
                except ValueError:
                    percent = 0.0
                # Calculate downloaded size in MiB
                downloaded_bytes = d.get('downloaded_bytes', 0)
                downloaded_mb = downloaded_bytes / (1024 * 1024)
                # Calculate speed manually
                time_delta = current_time - last_update if last_update else 0.1
                speed_mb_s = (downloaded_bytes - last_bytes) / (1024 * 1024 * time_delta) if time_delta > 0 else 0.0
                last_bytes = downloaded_bytes
                last_update = current_time
                # Update progress bar
                if pbar and pbar.total > 0 and total_size_mb > 0:
                    pbar.n = downloaded_mb
                elif pbar:
                    pbar.n = percent
                # Update postfix with ETA and speed
                eta = d.get('eta', 'Unknown')
                eta_str = f"ETA {time.strftime('%M:%S', time.gmtime(eta))}" if eta != 'Unknown' else 'ETA Unknown'
                if pbar:
                    pbar.set_postfix_str(f"{eta_str}, {speed_mb_s:.2f}MiB/s")
                    pbar.refresh()
        elif d['status'] == 'finished':
            if pbar:
                if pbar.total > 0:
                    pbar.n = pbar.total
                else:
                    pbar.n = 100
                pbar.refresh()
                pbar.close()
                pbar = None
            print(f"{Fore.GREEN}✅ Download complete: {d.get('filename', 'Unknown')}{Style.RESET_ALL}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': audio_quality if audio_quality != 'best' else '320',
        }],
        'ffmpeg_location': None,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
        'paths': {'home': str(AUDIO_DIR), 'temp': str(AUDIO_DIR)}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except yt_dlp.DownloadError as e:
        print(f"{Fore.RED}Error downloading {url}: {str(e)}{Style.RESET_ALL}")
        return False

# Download advanced
def download_advanced(url, format_str, subtitles, thumbnails, metadata, config):
    if not check_ffmpeg():
        return False
    
    # Determine if URL is a playlist
    with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': True}) as ydl:
        try:
            flat_info = ydl.extract_info(url, download=False)
            is_playlist = 'entries' in flat_info
        except yt_dlp.DownloadError as e:
            print(f"{Fore.RED}Error: Invalid link {url} - {str(e)}{Style.RESET_ALL}")
            return False
    
    if is_playlist:
        playlist_title = flat_info.get('title', 'Unknown Playlist')
        num_videos = len(flat_info['entries'])
        print(f"{Fore.BLUE}🎥 Playlist: {playlist_title}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📋 Number of videos: {num_videos}{Style.RESET_ALL}")
        if input(f"{Fore.CYAN}➤ Proceed with downloading playlist? (y/n): {Style.RESET_ALL}").strip().lower() != 'y':
            return False
        output_path = VIDEO_DIR / "%(title)s.%(ext)s"
        pbar = None
        video_count = 0
    else:
        # Single: fetch info with specified format for accurate size
        ydl_opts_info = {
            'format': format_str,
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl_info:
            info = ydl_info.extract_info(url, download=False)
        if not info:
            return False
        title = clean_filename(info['title'])
        output_path = VIDEO_DIR / f"{title}.%(ext)s"
        
        if not show_pre_download_info(info, format_str, str(output_path), format_str):
            return False
        total_size_mb = (info.get('filesize') or info.get('filesize_approx') or 0) / (1024 * 1024)
        pbar = create_progress_bar(total_size_mb, title)
        video_count = 0
    
    last_update = 0
    last_bytes = 0
    current_title = ""
    
    def progress_hook(d):
        nonlocal pbar, last_update, last_bytes, current_title, video_count
        current_time = time.time()
        if d['status'] == 'downloading':
            # Get current video title
            title = d.get('info_dict', {}).get('title', 'Unknown')
            total_size_mb = (d.get('info_dict', {}).get('filesize') or d.get('info_dict', {}).get('filesize_approx') or 0) / (1024 * 1024)
            if title != current_title:
                if pbar:
                    pbar.close()
                video_count += 1
                current_title = title
                desc = f"Video {video_count}/{num_videos}: {title[:30]}" if is_playlist else title[:30]
                pbar = create_progress_bar(total_size_mb, desc)
            
            # Update every 0.1 seconds
            if current_time - last_update >= 0.1:
                # Strip ANSI codes from _percent_str
                percent_str = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', d.get('_percent_str', '0%')).strip('%')
                try:
                    percent = float(percent_str)
                except ValueError:
                    percent = 0.0
                # Calculate downloaded size in MiB
                downloaded_bytes = d.get('downloaded_bytes', 0)
                downloaded_mb = downloaded_bytes / (1024 * 1024)
                # Calculate speed manually
                time_delta = current_time - last_update if last_update else 0.1
                speed_mb_s = (downloaded_bytes - last_bytes) / (1024 * 1024 * time_delta) if time_delta > 0 else 0.0
                last_bytes = downloaded_bytes
                last_update = current_time
                # Update progress bar
                if pbar and pbar.total > 0 and total_size_mb > 0:
                    pbar.n = downloaded_mb
                elif pbar:
                    pbar.n = percent
                # Update postfix with ETA and speed
                eta = d.get('eta', 'Unknown')
                eta_str = f"ETA {time.strftime('%M:%S', time.gmtime(eta))}" if eta != 'Unknown' else 'ETA Unknown'
                if pbar:
                    pbar.set_postfix_str(f"{eta_str}, {speed_mb_s:.2f}MiB/s")
                    pbar.refresh()
        elif d['status'] == 'finished':
            if pbar:
                if pbar.total > 0:
                    pbar.n = pbar.total
                else:
                    pbar.n = 100
                pbar.refresh()
                pbar.close()
                pbar = None
            print(f"{Fore.GREEN}✅ Download complete: {d.get('filename', 'Unknown')}{Style.RESET_ALL}")

    ydl_opts = {
        'format': format_str,
        'outtmpl': str(output_path),
        'merge_output_format': 'mp4',
        'ffmpeg_location': None,
        'writesubtitles': subtitles,
        'writethumbnail': thumbnails,
        'embedthumbnail': thumbnails and metadata,
        'addmetadata': metadata,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
        'paths': {'home': str(VIDEO_DIR), 'temp': str(VIDEO_DIR)}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"{Fore.GREEN}✅ Download complete: {output_path}{Style.RESET_ALL}")
        return True
    except yt_dlp.DownloadError as e:
        print(f"{Fore.RED}Error downloading {url}: {str(e)}{Style.RESET_ALL}")
        return False

# Main function
def main():
    config = load_config()
    links = get_links()
    if not links:
        return
    
    download_type = choose_download_type(config)
    
    if download_type == '1':
        quality = choose_video_quality(config)
    elif download_type == '2':
        audio_quality = choose_audio_quality(config)
    else:
        format_str, subtitles, thumbnails, metadata = choose_advanced_options(config)
    
    successes = 0
    for url in links:
        print(f"{Fore.YELLOW}Processing: {url}{Style.RESET_ALL}")
        success = False
        if download_type == '1':
            success = download_video(url, quality, config)
        elif download_type == '2':
            success = download_audio(url, audio_quality, config)
        else:
            success = download_advanced(url, format_str, subtitles, thumbnails, metadata, config)
        successes += 1 if success else 0
    
    print(f"{Fore.YELLOW}{'='*24}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Completed: {successes}/{len(links)} links downloaded successfully.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()