#!/bin/sh

if [ "$DATABASE_FRONT" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST_FRONT $SQL_PORT_FRONT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate

exec "$@"