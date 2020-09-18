from __future__ import unicode_literals

from urllib.parse import urlparse

import youtube_dl


STORE_PATH = "/tmp"
FORMAT = "mp3"

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

    if parsed_url.netloc == "www.youtube.com":
        return url

    raise NonYouTubeUrlError


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
