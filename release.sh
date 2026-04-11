#!/bin/bash
set -e

cd src

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Release script completed"
