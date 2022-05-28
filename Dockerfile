# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN python3 -m venv .venv

COPY requirements.txt .

RUN . .venv/bin/activate && pip3 install -r requirements.txt

COPY weights/ weights/

COPY templates/ templates/

COPY app.py .

CMD . .venv/bin/activate && gunicorn -w 4 -b $BIND:$PORT app:app