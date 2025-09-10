#!/usr/bin/env bash
# exit on error
set -o errexit  

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput


# Create a superuser non-interactively if environment variables are set
if [[ $DJANGO_SUPERUSER_USERNAME && $DJANGO_SUPERUSER_PASSWORD ]]; then
  python manage.py createsuperuser --no-input
fi

# Run migrations
python manage.py migrate
# Apply database migrations
python manage.py migrate
