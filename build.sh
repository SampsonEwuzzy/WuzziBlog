#!/usr/bin/env bash
set -o errexit  

pip install -r requirements.txt

python manage.py collectstatic --noinput

if [[ $DJANGO_SUPERUSER_USERNAME && $DJANGO_SUPERUSER_PASSWORD ]]; then
  python manage.py createsuperuser --no-input
fi

python manage.py migrate

