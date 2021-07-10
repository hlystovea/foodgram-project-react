FROM python:3.8.5
WORKDIR /code
COPY requirements.txt /code
RUN pip3 install -r /code/requirements.txt
COPY ./backend /code
RUN chmod +x *.sh
CMD gunicorn project.wsgi:application --bind 0.0.0.0:8000
