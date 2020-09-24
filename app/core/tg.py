import os
from tempfile import TemporaryDirectory

import telebot

from .default_logging import file_logger
from .settings import API_TOKEN
from .youtube_handler import (
    NonYouTubeUrlError,
    VideoProcessingError,
    get_audio_from_video,
    split_audio,
    validate_url,
)


START_MSG = (
    "Welcome to Podcastinate Bot! "
    "Send me link to YouTube video and I'll send you audio from it back."
)
HELP_MSG = "Send YouTube link to Bot and get audio back."
INVALID_LINK_MSG = "It's not YouTube link, try again."
PROCESSING_ERROR_MSG = "Processing error. Check your link and try again later."


bot = telebot.TeleBot(API_TOKEN)


def send_audio(filepath, title, uploader, chat_id):
    with open(filepath, "rb") as audio:
        bot.send_audio(chat_id, audio, caption=title, title=title, performer=uploader)
    try:
        os.remove(filepath)
    except OSError:
        pass


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, START_MSG)


@bot.message_handler(commands=["help"])
def start_message(message):
    bot.send_message(message.chat.id, HELP_MSG)


@bot.message_handler(func=lambda message: True)
def process_message(message):
    url = message.text

    try:
        validate_url(url)
    except NonYouTubeUrlError:
        bot.send_message(message.chat.id, INVALID_LINK_MSG)
        return

    try:
        filepath, title, uploader = get_audio_from_video(url)

        if os.path.getsize(filepath) < 50 * 1024 * 1024:
            send_audio(filepath, title, uploader, message.chat.id)
            file_logger.info(
                f"{message.message_id} - response: "
                f"{{ uploader: {uploader}, title: {title} }}"
            )
        else:
            with TemporaryDirectory() as tpm_dir:
                splitted_audio = split_audio(filepath, tpm_dir)
                for number, file_part in enumerate(splitted_audio):
                    part_title = f"{title}. Part {number}"
                    send_audio(file_part, part_title, uploader, message.chat.id)
                    file_logger.info(
                        f"{message.message_id} - response: "
                        f"{{ uploader: {uploader}, title: {part_title} }}"
                    )

    except VideoProcessingError:
        bot.send_message(message.chat.id, PROCESSING_ERROR_MSG)
