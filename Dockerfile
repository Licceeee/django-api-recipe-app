FROM python:3.8-alpine
LABEL Alicia Schonefeld

ENV PYTHONUNBUFFED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D dockeruser
USER dockeruser

