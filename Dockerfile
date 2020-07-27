FROM python:3.8-alpine
LABEL Alicia Schonefeld

ENV PYTHONUNBUFFED 1

COPY ./requirements.txt /requirements.txt
# permament dependencies
RUN apk add --update --no-cache postgresql-client jpeg-dev
# temporary dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev \
        linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D dockeruser
RUN chown -R dockeruser:dockeruser /vol/
RUN chmod -R 755 /vol/web
USER dockeruser