FROM python:3.10.8-alpine3.16

RUN apk add --no-cache jpeg-dev postgresql-libs && \
    apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev \
    g++ \
    python3-dev \
    zlib-dev \
    libxml2-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    build-base


WORKDIR /code

COPY . /code/

RUN pip install -r requirements.txt
