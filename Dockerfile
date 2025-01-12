FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bot

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev \
    openssl

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY /bot/* /bot/

RUN alembic upgrade head
