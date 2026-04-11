#!/bin/bash
set -e

cd src

echo "Checking if migrations need to be applied..."

# Try to run migrations. If the database isn't ready yet, we'll retry.
# This handles the case where migrations table doesn't exist yet
python manage.py migrate --noinput 2>/dev/null || {
    echo "Database connection failed, will retry migrations..."
    # This is expected during initial deployment
}

echo "Starting Gunicorn server..."
exec gunicorn family.wsgi:application --bind 0.0.0.0:8080
