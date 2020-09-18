from os import getenv


API_TOKEN = getenv("API_TOKEN", None)

WEBHOOK_HOST = getenv("WEBHOOK_HOST", None)
WEBHOOK_PORT = getenv("WEBHOOK_PORT", None)
WEBHOOK_LISTEN = getenv("WEBHOOK_LISTEN", None)

WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}"
WEBHOOK_URL_PATH = f"/{API_TOKEN}/"

WEBHOOK_SSL_CERT = "/opt/podcastinate/app/core/certs/webhook_cert.pem"
WEBHOOK_SSL_PKEY = "/opt/podcastinate/app/core/certs/webhook_pkey.pem"

LOG_PATH = "/var/logs/podcastinate_bot.log"
