FROM python:3.8-alpine
LABEL maintainer="Max Terin"

WORKDIR /opt/podcastinate/app
RUN mkdir /var/logs \
&& apk update && apk add  --no-cache ffmpeg

COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app/core core
COPY app/run.py run.py
COPY app/runfiles runfiles

CMD ["/bin/sh"]
