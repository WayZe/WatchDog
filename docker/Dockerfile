FROM python:3.9-rc-alpine3.12

RUN apk update
RUN pip install --upgrade pip requests python-dotenv pytelegrambotapi

COPY app /opt/app
COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

WORKDIR /opt

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
