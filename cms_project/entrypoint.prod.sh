#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! python -c "import socket; s = socket.socket(); s.settimeout(1); s.connect(('$SQL_HOST', int('$SQL_PORT')))" 2>/dev/null; 
    do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$SKIP_MIGRATIONS" != "true" ]
then
    echo "Syncing core database structure..."
    python manage.py migrate --schema=public

    echo "Running tenant database migrations..."
    python manage.py migrate_schemas --shared
    python manage.py migrate_schemas --tenant
fi

echo "Collecting static files..."
python manage.py collectstatic --no-input

# Passa o controle para o CMD (Gunicorn)
exec "$@"