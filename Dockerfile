# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN python3 -m venv .venv

COPY requirements.txt .

RUN . .venv/bin/activate && pip3 install -r requirements.txt

COPY weights/ weights/

COPY app.py .

COPY templates/ templates/

CMD . .venv/bin/activate && python app.py