from pathlib import Path

from yt_dlp import YoutubeDL

from config import app_settings
from config.log_config import logger


class VideoDownloader:
    """
    Downloads and converts videos using yt_dlp with predefined options.
    """

    __ydl_opts = {
        "format": "bv*+ba/best[ext=mp4]/best",
        "outtmpl": str(Path(app_settings.get_full_temp_path(), "%(title)s.%(ext)s")),
        "recode_video": "mp4",
        "postprocessor_args": [
            "-vf",
            "scale=-2:480",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "27",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
        ],
        "concurrent_fragment_downloads": 4,
        "quiet": app_settings.suppress_download_logs,
    }

    filename: str | None = None

    @classmethod
    def download(cls, url: str):
        """
        Download and convert a video from the given URL using yt_dlp.

        Args:
            url (str): The video URL to download.
        """

        with YoutubeDL(cls.__ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            cls.filename = filename
            logger.info(f"Saved to: {filename}")
