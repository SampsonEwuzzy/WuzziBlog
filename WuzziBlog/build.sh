#!/usr/bin/env bash
# exit on error
set -o errexit  

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput


python manage.py migrate
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

# Apply database migrations
python manage.py migrate
