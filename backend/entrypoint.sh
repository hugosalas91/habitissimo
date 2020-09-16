#!/bin/sh

if [ "$DATABASE_BACK" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST_BACK $SQL_PORT_BACK; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py create_super_user
python manage.py create_anonymous_user
python manage.py fill_jobs
python manage.py initialize_backpack_challenge
python manage.py initialize_example_backpack

exec "$@"