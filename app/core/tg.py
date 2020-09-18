import os

import telebot

from .settings import API_TOKEN
from .default_logging import file_logger
from .youtube_handler import (
    NonYouTubeUrlError,
    VideoProcessingError,
    get_audio_from_video,
    validate_url,
)


START_MSG = (
    "Welcome to Podcastinate Bot! "
    "Send me link to YouTube video and I'll send you audio from it back."
)
HELP_MSG = """Send YouTube video link to Bot and get audio from it back."""
INVALID_LINK_MSG = "This is not YouTube video link, please try again."
PROCESSING_ERROR_MSG = "Processing error. Check your link and try again later."


bot = telebot.TeleBot(API_TOKEN)


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
        with open(filepath, "rb") as audio:
            bot.send_audio(
                message.chat.id, audio, caption=title, title=title, performer=uploader
            )
            file_logger.info(f"{message.message_id} - {uploader} - {title}")
        try:
            os.remove(filepath)
        except OSError:
            pass
    except VideoProcessingError:
        bot.send_message(message.chat.id, PROCESSING_ERROR_MSG)
