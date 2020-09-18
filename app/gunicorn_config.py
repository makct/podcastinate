bind = "0.0.0.0:5000"
workers = 2
worker_class = "sync"
preload = True
max_requests = 1000
loglevel = "info"
daemon = False
reload = False
certfile = "/opt/podcastinate/app/core/certs/webhook_cert.pem"
keyfile = "/opt/podcastinate/app/core/certs/webhook_pkey.pem"
