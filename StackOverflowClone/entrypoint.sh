#!/bin/bash
echo 'ENTRY POINT FILE HAS BEEN RUNNED SUCCESSFULLY'
APP_PORT=${PORT:-8000}
cd /app/
/opt/venv/bin/python manage.py collectstatic --noinput
echo 'static collected'
echo 'MIGRATATION STARTED!!'
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"hbpatel7687@gmail.com"}
cd /app/

/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true

echo 'MIGRATATION FINISHEDDDDDD!!'
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm StackOverflowClone.asgi:application --bind "0.0.0.0:${APP_PORT}" -k uvicorn.workers.UvicornWorker
