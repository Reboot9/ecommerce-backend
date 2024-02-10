#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE=ecommerce_backend.settings.local

./wait-for-it.sh $DB_HOST:$DB_PORT -t 60

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply django migrations
until python3 manage.py migrate
do
  echo "Waiting for the database to be ready..."
  sleep 2
done

echo "Database is ready. Starting the development server..."

# Wait for Nginx to become ready
./wait-for-it.sh nginx:80 -- echo "Nginx is ready to accept connections."

# Start the development server
gunicorn ecommerce_backend.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4

exec "$@"
