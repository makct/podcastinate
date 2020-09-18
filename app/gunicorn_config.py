from core.settings import WEBHOOK_SSL_CERT, WEBHOOK_SSL_PKEY

bind = "0.0.0.0:5000"
workers = 1
worker_class = "sync"
preload = True
max_requests = 1000
timeout = 300
loglevel = "info"
daemon = False
reload = False
certfile = WEBHOOK_SSL_CERT
keyfile = WEBHOOK_SSL_PKEY
