FROM python:3.9-slim-buster
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./backend .
