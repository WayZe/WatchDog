FROM python:3.9-rc-alpine3.12

COPY app /opt/app
COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

WORKDIR /opt

RUN apk update && \
    apk add --no-cache && \
    pip install --upgrade pip requests bs4 && \
    chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
