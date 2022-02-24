FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
  tor \
  && rm -rf /var/lib/apt/lists/*

ADD torrc /etc/tor/torrc

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
