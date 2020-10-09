FROM python:3.9-rc-alpine3.12

RUN apk update
RUN pip install --upgrade pip requests python-dotenv pytelegrambotapi

COPY app /opt/app

WORKDIR /opt

ENTRYPOINT ["python", "app/api.py"]
