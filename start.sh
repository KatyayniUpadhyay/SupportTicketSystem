#!/bin/sh

# Wait for database to be fully ready (extra safety)
echo "Running migrations..."
python manage.py migrate --noinput

# Start the server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000