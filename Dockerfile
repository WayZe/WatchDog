FROM python:3.7.3-alpine3.9

COPY . /app/

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install requests bs4 && \
    chmod +x docker-entrypoint.sh

ENTRYPOINT ["sh", "docker-entrypoint.sh"]