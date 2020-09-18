from __future__ import unicode_literals

import os
from typing import List
from urllib.parse import urlparse

import youtube_dl
from pydub import AudioSegment


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


def split_audio(filepath) -> List[str]:
    time_period = 50 * 60 * 1000

    if os.path.getsize(filepath) < 50 * 1024 * 1024:
        return [filepath]

    audio = AudioSegment.from_mp3(filepath)

    filename = os.path.basename(filepath).split(".")[0]

    splitted_files = []
    pos = 0

    for i in range(len(audio) // time_period + 1):
        audio_part = audio[pos : pos + time_period]
        pos = pos + time_period
        filename = f"/tmp/{filename}_part{i}.{FORMAT}"
        audio_part.export(filename, format=FORMAT)
        splitted_files.append(filename)

    return splitted_files


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
