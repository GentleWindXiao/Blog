#!/usr/bin/env bash
set -e

if [ -n "" ]; then
  echo "Waiting for database at :..."
  for i in {1..60}; do
    if nc -z  ; then
      echo "Database is up!"; break
    fi
    echo "...retry ()"; sleep 1
  done
fi

python manage.py migrate --noinput

exec gunicorn blog_project.wsgi:application \
  --config /app/gunicorn.conf.py
