import os

import telebot

from .settings import API_TOKEN
from .youtube_handler import (
    NonYouTubeUrlError,
    VideoProcessingError,
    get_audio_from_video,
    validate_url,
)


bot = telebot.TeleBot(API_TOKEN)


HELP_MESSAGE = """Send YouTube video link to Bot and get audio from it back."""
INVALID_LINK_ERR = "This is not YouTube video link, please try again."


@bot.message_handler(commands=["start"])
def start_message(message):
    msg = (
        "Welcome to Podcastinate Bot! "
        "Send me link to YouTube video and I'll send you audio from it back."
    )
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["help"])
def start_message(message):
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.message_handler(func=lambda message: True)
def process_message(message):
    url = message.text
    try:
        validate_url(url)
    except NonYouTubeUrlError:
        bot.send_message(message.chat.id, INVALID_LINK_ERR)

    try:
        filepath, title = get_audio_from_video(url)
        bot.send_audio(message.chat.id, filepath, title=title)
        os.remove(filepath)
    except VideoProcessingError:
        bot.send_message(
            message.chat.id, "Processing error. Check your link and try later."
        )
