#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE=ecommerce_backend.settings.local

python manage.py collectstatic --noinput

# Apply migrations
until python3 manage.py migrate
do
  echo "Waiting for database to be ready"
done

# Start the development server
gunicorn ecommerce_backend.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4

exec $@
