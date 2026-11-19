#!/usr/bin/env python3
"""Advanced Video Downloader powered by yt-dlp.

Use only for media you own or have permission to download.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yt_dlp


def progress_hook(data):
    status = data.get("status")
    if status == "downloading":
        percent = data.get("_percent_str", "").strip()
        speed = data.get("_speed_str", "").strip()
        eta = data.get("_eta_str", "").strip()
        print(f"\rDownloading {percent} | {speed} | ETA {eta}", end="", flush=True)
    elif status == "finished":
        print("\nDownload complete. Processing media...")


def build_options(args):
    output = Path(args.output).expanduser()
    output.mkdir(parents=True, exist_ok=True)

    if args.audio_only:
        media_format = "bestaudio/best"
    elif args.quality == "best":
        media_format = "bestvideo*+bestaudio/best"
    else:
        height = int(args.quality.removesuffix("p"))
        media_format = (
            f"bestvideo*[height<={height}]+bestaudio/"
            f"best[height<={height}]/best"
        )

    options = {
        "format": media_format,
        "outtmpl": str(output / "%(title).180B [%(id)s].%(ext)s"),
        "noplaylist": not args.playlist,
        "retries": args.retries,
        "fragment_retries": args.retries,
        "continuedl": True,
        "windowsfilenames": True,
        "progress_hooks": [progress_hook],
        "concurrent_fragment_downloads": args.fragments,
        "merge_output_format": "mp4",
    }

    if args.audio_only:
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": args.audio_format,
            "preferredquality": "0",
        }]

    if args.cookies:
        options["cookiefile"] = args.cookies

    if args.proxy:
        options["proxy"] = args.proxy

    return options


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Advanced video downloader powered by yt-dlp. "
            "Download only media you are authorized to save."
        )
    )
    parser.add_argument("urls", nargs="*", help="One or more video URLs")
    parser.add_argument("-o", "--output", default="downloads", help="Output folder")
    parser.add_argument(
        "-q",
        "--quality",
        choices=["best", "2160p", "1440p", "1080p", "720p", "480p", "360p"],
        default="best",
        help="Maximum video quality",
    )
    parser.add_argument("--playlist", action="store_true", help="Allow playlist downloads")
    parser.add_argument("--audio-only", action="store_true", help="Download audio only")
    parser.add_argument(
        "--audio-format",
        choices=["mp3", "m4a", "opus", "wav"],
        default="mp3",
    )
    parser.add_argument("--cookies", help="Netscape-format cookies file")
    parser.add_argument("--proxy", help="Proxy URL supported by yt-dlp")
    parser.add_argument("--retries", type=int, default=10)
    parser.add_argument("--fragments", type=int, default=4)
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.urls:
        try:
            url = input("Video URL: ").strip()
        except (EOFError, KeyboardInterrupt):
            return 1
        if not url:
            print("No URL supplied.", file=sys.stderr)
            return 2
        args.urls = [url]

    try:
        with yt_dlp.YoutubeDL(build_options(args)) as downloader:
            return int(downloader.download(args.urls) or 0)
    except yt_dlp.utils.DownloadError as exc:
        print(f"\nDownload failed: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
