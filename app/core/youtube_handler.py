from __future__ import unicode_literals

import os
import pathlib
import subprocess
from typing import List
from urllib.parse import urlparse

import youtube_dl


STORE_PATH = "/tmp"
FORMAT = "mp3"
ALLOWED_HOSTS = ["youtu.be", "www.youtube.com"]

ydl_opts = {
    "outtmpl": f"{STORE_PATH}/%(id)s.%(ext)s",
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": FORMAT,
            "preferredquality": "192",
        }
    ],
}


class NonYouTubeUrlError(Exception):
    pass


class VideoProcessingError(Exception):
    pass


def validate_url(url):
    parsed_url = urlparse(url)

    if parsed_url.netloc in ALLOWED_HOSTS:
        return url

    raise NonYouTubeUrlError


def split_audio(filepath, tmp_dir) -> List[str]:
    file_name = os.path.basename(filepath).split(".")[0]

    command = (
        f"ffmpeg -i {filepath} -f segment -segment_time 2000 -c copy "
        f"{tmp_dir}/{file_name}_part%01d.mp3 -hide_banner -loglevel panic"
    )
    process = subprocess.run(command.split())

    if process.returncode != 0:
        raise VideoProcessingError

    return sorted([str(file) for file in pathlib.Path(tmp_dir).glob("**/*")])


def get_audio_from_video(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(url)
        except youtube_dl.utils.YoutubeDLError as err:
            raise VideoProcessingError

    return (
        f"{STORE_PATH}/{result.get('id')}.{FORMAT}",
        result.get("title"),
        result.get("uploader"),
    )
