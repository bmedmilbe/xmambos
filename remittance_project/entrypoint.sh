#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! python -c "import socket; s = socket.socket(); s.settimeout(1); s.connect(('$SQL_HOST', int('$SQL_PORT')))"
    do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# RUN THE DJANGO PRODUCTION COMMANDS HERE
# echo "Running database migrations..."
# python manage.py migrate_schemas --shared
# python manage.py migrate_schemas --tenant

exec "$@"