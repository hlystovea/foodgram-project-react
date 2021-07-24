#!/bin/bash

set -e

sleep 10

echo "${0}: running migrations."
python manage.py migrate --noinput

echo "${0}: collecting statics."
python manage.py collectstatic --noinput
