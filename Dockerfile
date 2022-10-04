FROM python:3.10

RUN apt-get update
RUN apt-get install -y postgresql-client

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY requirements.txt /bot/requirements.txt
RUN pip install -r requirements.txt
