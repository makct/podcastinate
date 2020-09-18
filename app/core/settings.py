from os import getenv


# MYSQL_HOST = getenv("MYSQL_HOST", None)
# MYSQL_PORT = getenv("MYSQL_PORT", None)
# MYSQL_USER = getenv("MYSQL_USER", None)
# MYSQL_PASSWORD = getenv("MYSQL_PASSWORD", None)
# MYSQL_DB = getenv("MYSQL_DB", None)

API_TOKEN = getenv("API_TOKEN", None)

WEBHOOK_HOST = getenv("WEBHOOK_HOST", None)
WEBHOOK_PORT = getenv("WEBHOOK_PORT", None)
WEBHOOK_LISTEN = getenv("WEBHOOK_LISTEN", None)

WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}"
WEBHOOK_URL_PATH = f"/{API_TOKEN}/"

WEBHOOK_SSL_CERT = "/opt/podcastinate/app/core/certs/webhook_cert.pem"
WEBHOOK_SSL_PKEY = "/opt/podcastinate/app/core/certs/webhook_pkey.pem"

LOG_PATH = "/var/logs/podcastinate_bot.log"
