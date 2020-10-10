FROM python:3.9-rc-alpine3.12

RUN apk update

COPY requirements.txt .

RUN pip install --upgrade pip -r requirements.txt

COPY app /opt/app

WORKDIR /opt

ENTRYPOINT ["python", "app/api.py"]
