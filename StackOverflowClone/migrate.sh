#!/bin/bash
echo 'MIGRATE FILE HAS BEEN RUNNED SUCCESSFULLY'
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"hbpatel7687@gmail.com"}
cd /app/
/opt/venv/bin/python manage.py makemigrations --noinput
/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true
