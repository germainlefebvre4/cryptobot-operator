FROM python:3.7-slim

COPY . .

RUN apt update && \
    apt install -y build-essential libssl-dev libffi-dev && \
    pip install -r requirements.txt && \
    apt clean

CMD kopf run main.py
