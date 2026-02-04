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

def get_common_opts():
    """Returns base options to bypass 403 Forbidden errors."""
    return {
        'quiet': True,
        'no_warnings': True,
        # Authenticates the request using your browser's session
        'cookiesfrombrowser': ('chrome',), 
        # Makes the request look like a standard desktop browser
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
    }

def get_filesize(url, resolution=None, format_type="mp4"):
    """Print approximate file size without downloading."""
    ydl_opts = get_common_opts()
    
    if format_type == "mp3":
        ydl_opts['format'] = 'bestaudio/best'
    elif format_type == "mp4":
        ydl_opts['format'] = f'bestvideo[height<={resolution or 1080}][ext=mp4]+bestaudio/best'
    else:
        ydl_opts['format'] = f'bestvideo[height<={resolution or 1080}]+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filesize = info.get('filesize_approx') or info.get('filesize')
            if filesize:
                print(f"Approx. size: {round(filesize / (1024*1024), 2)} MB")
    except Exception as e:
        print(f"Error fetching info: {e}")

def download_video(url, resolution=None, format_type="mp4"):
    ydl_opts = get_common_opts()
    ydl_opts.update({
        'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
    })

    if format_type == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif format_type == "mp4":
        res_str = f'[height<={resolution}]' if resolution else ''
        ydl_opts.update({
            'format': f'bestvideo{res_str}[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        })
    else:  # webm
        res_str = f'[height<={resolution}]' if resolution else ''
        ydl_opts.update({
            'format': f'bestvideo{res_str}+bestaudio/best',
        })

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