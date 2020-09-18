import time

import flask
import telebot
from core.settings import (
    WEBHOOK_LISTEN,
    WEBHOOK_PORT,
    WEBHOOK_SSL_CERT,
    WEBHOOK_SSL_PKEY,
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
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(2)

# Set webhook
bot.set_webhook(
    url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, "r")
)

# Start flask server
app.run(
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PKEY),
    debug=True,
)
