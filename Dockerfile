FROM python:3.9
WORKDIR /foodgram
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./backend .
