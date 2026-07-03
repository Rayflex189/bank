#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput 

echo "Creating admin..."
python manage.py create_admin

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn wealthbridge.wsgi:application --bind 0.0.0.0:8088