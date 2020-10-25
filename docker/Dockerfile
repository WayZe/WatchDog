FROM python:3.9-rc-alpine3.12

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .

RUN pip install --upgrade pip -r requirements.txt

COPY app /opt/app
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh

WORKDIR /opt

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT [ "entrypoint.sh" ]
