FROM python:3.8-alpine

ENV PYTHONBUFFERED 1

RUN mkdir /aiohttp-crud
WORKDIR /aiohttp-crud
COPY . /aiohttp-crud

RUN apk add --no-cache screen postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc g++ musl-dev postgresql-dev && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

RUN ["chmod", "+x", "/aiohttp-crud/start.sh"]
CMD /aiohttp-crud/start.sh