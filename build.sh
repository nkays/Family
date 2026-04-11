#!/bin/bash
set -e

cd src

# Collect static files without requiring database access
# This uses --noinput to skip interactive prompts and handles missing apps gracefully
python manage.py collectstatic --noinput --ignore=node_modules --clear 2>/dev/null || true

echo "Build script completed"
