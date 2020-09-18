import json
import time

import flask
import telebot

from core.default_logging import file_logger
from core.settings import (
    WEBHOOK_SSL_CERT,
    WEBHOOK_URL_BASE,
    WEBHOOK_URL_PATH,
)
from core.tg import bot


app = flask.Flask(__name__)


@app.route("/", methods=["GET", "HEAD"])
def index():
    return ""


@app.route(WEBHOOK_URL_PATH, methods=["POST"])
def webhook():
    if flask.request.headers.get("content-type") == "application/json":
        json_string = flask.request.get_data().decode("utf-8")

        msg = json.loads(json_string)["message"]
        file_logger.info(
            f"{msg['message_id']} - request: "
            f"{{ from: {msg['from']['username']}, text: {msg['text']} }}"
        )

        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)


bot.remove_webhook()

time.sleep(2)

bot.set_webhook(
    url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, "r")
)
