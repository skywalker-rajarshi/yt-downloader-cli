import os
import sys
import argparse
import yt_dlp

downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads/ytvideos")
os.makedirs(downloads_folder, exist_ok=True)

def progress_hook(d):
    """Display a terminal progress bar based on bytes downloaded."""
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        speed = d.get('_speed_str', '').strip()
        eta = d.get('_eta_str', '').strip()

        if total:
            percent_float = downloaded / total * 100
            bar_len = 40
            filled_len = int(bar_len * percent_float / 100)
            bar = '█' * filled_len + '-' * (bar_len - filled_len)
            sys.stdout.write(f"\r[{bar}] {percent_float:5.1f}% at {speed} ETA {eta}")
            sys.stdout.flush()
    elif d['status'] == 'finished':
        sys.stdout.write("\nDownload complete!\n")

def get_filesize(url, resolution=None, format_type="mp4"):
    """Print approximate file size without downloading."""
    ydl_opts = {}
    if format_type == "mp3":
        ydl_opts['format'] = 'bestaudio/best'
    elif format_type == "mp4":
        if resolution:
            ydl_opts['format'] = f'bestvideo[height<={resolution}][ext=mp4]+bestaudio/best'
        else:
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio/best'
    else:  # webm
        if resolution:
            ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best'
        else:
            ydl_opts['format'] = 'best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filesize = info.get('filesize_approx') or info.get('filesize')
        if filesize:
            print(f"Approx. size: {round(filesize / (1024*1024), 2)} MB")

def download_video(url, resolution=None, format_type="mp4"):
    if format_type == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
    elif format_type == "mp4":
        if resolution:
            fmt = f'bestvideo[height<={resolution}][ext=mp4]+bestaudio/best'
        else:
            fmt = 'bestvideo[ext=mp4]+bestaudio/best'
        ydl_opts = {
            'format': fmt,
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],
            'quiet': True,
        }
    else:  # webm
        if resolution:
            fmt = f'bestvideo[height<={resolution}]+bestaudio/best'
        else:
            fmt = 'best'
        ydl_opts = {
            'format': fmt,
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
            'merge_output_format': None,
            'progress_hooks': [progress_hook],
            'quiet': True,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Downloader CLI (mp4/mp3/webm) with QuickTime support and progress bar"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-r", "--resolution", type=int, help="Max resolution (e.g., 720, 1080)")
    parser.add_argument("-f", "--format", choices=["mp4", "mp3", "webm"], default="mp4",
                        help="Download format (mp4, mp3, or webm)")
    args = parser.parse_args()

    get_filesize(args.url, args.resolution, args.format)
    download_video(args.url, args.resolution, args.format)

if __name__ == "__main__":
    main()
