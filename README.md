yt-downloader-cli
A lightweight command-line interface for downloading YouTube videos in MP4, MP3, or WebM formats with a terminal progress bar and QuickTime compatibility.

Features
Multiple Formats: Download as high-quality MP4, extract audio to MP3, or use WebM.

Resolution Control: Specify maximum resolution (e.g., 720, 1080).

Size Estimation: View the approximate file size before the download begins.

Progress Tracking: Includes a visual terminal progress bar with download speed and ETA.

Enhanced Compatibility: Uses browser cookies and custom User-Agents to bypass common 403 Forbidden errors.

Installation Guide
Prerequisites

Python: Version 3.10 or higher.

FFmpeg: Required for audio extraction (MP3) and merging video/audio streams.

Setup

Clone the Repository (or navigate to the project directory):

Bash
cd yt-downloader-cli
Install via Pip: You can install the tool and its dependencies directly from the project folder:

Bash
pip install .
This will install the required yt-dlp library and register the yt-downloader command to your system.

Usage
Once installed, use the yt-downloader command followed by a YouTube URL.

Basic Download (Default MP4)

Bash
yt-downloader "https://www.youtube.com/watch?v=example"
Download as MP3 (Audio Only)

Bash
yt-downloader "https://www.youtube.com/watch?v=example" -f mp3
Specify Resolution

To limit the download to 720p:

Bash
yt-downloader "https://www.youtube.com/watch?v=example" -r 720
Options

Argument	Description
url	The YouTube video URL (Required).
-f, --format	Format to download: mp4, mp3, or webm (Default: mp4).
-r, --resolution	Max resolution, such as 720 or 1080.
Configuration
Download Location: By default, videos are saved to ~/Downloads/ytvideos. The tool will automatically create this directory if it does not exist.

Cookie Authentication: This tool is configured to use cookies from the Chrome browser to authenticate requests, which helps in accessing restricted content and avoiding bot detection.

License
This project is licensed under the GNU General Public License v2.0.
