# Advanced Video Downloader

A Python command-line video downloader powered by **yt-dlp**.

> Use this project only for media you own, public-domain media, or content you otherwise have permission to download. Respect copyright, privacy, website terms, and applicable law.

## Features

- Interactive URL entry or command-line URLs
- Best quality or 2160p / 1440p / 1080p / 720p / 480p / 360p limits
- Video + audio merging with FFmpeg
- Audio-only downloads
- Resume and retry support
- Concurrent fragment downloading
- Optional playlist mode
- Optional Netscape cookies file for authorized sessions
- Optional proxy
- Windows-safe filenames
- Download percentage, speed, and ETA

## Requirements

- Python 3.10+
- FFmpeg (recommended; required for many merges and audio conversions)

## Installation

```bash
git clone https://github.com/Joshhacker25/advanced-video-downloader.git
cd advanced-video-downloader
python -m pip install -r requirements.txt
```

Install FFmpeg separately and ensure `ffmpeg` is available on your PATH.

## Usage

Interactive mode:

```bash
python downloader.py
```

Download a URL:

```bash
python downloader.py "VIDEO_URL"
```

Limit quality to 1080p:

```bash
python downloader.py "VIDEO_URL" -q 1080p
```

Choose a folder:

```bash
python downloader.py "VIDEO_URL" -o videos
```

Audio only:

```bash
python downloader.py "VIDEO_URL" --audio-only --audio-format mp3
```

Multiple URLs:

```bash
python downloader.py "URL_1" "URL_2" "URL_3"
```

Authorized cookies file:

```bash
python downloader.py "VIDEO_URL" --cookies cookies.txt
```

For every option:

```bash
python downloader.py --help
```

## Keeping extractor support current

Websites change frequently. Update yt-dlp when extraction stops working:

```bash
python -m pip install -U yt-dlp
```

## Notes

This project does not implement DRM or access-control circumvention. Site support depends on the installed yt-dlp version and the site's current behavior.
