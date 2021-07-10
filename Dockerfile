FROM python:3.8.5
WORKDIR /code/backend
COPY requirements.txt /code
RUN pip3 install -r /code/requirements.txt
COPY . /code
CMD gunicorn project.wsgi:application --bind 0.0.0.0:8000
