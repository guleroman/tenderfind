FROM python:3.6

ADD requirements.txt /app/requirements.txt

USER root
WORKDIR /app/

RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' app