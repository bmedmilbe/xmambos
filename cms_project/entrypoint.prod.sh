#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    # The '2>/dev/null' at the end keeps your terminal clean while waiting
    while ! python -c "import socket; s = socket.socket(); s.settimeout(1); s.connect(('$SQL_HOST', int('$SQL_PORT')))" 2>/dev/null; 
    do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# # RUN THE DJANGO PRODUCTION COMMANDS HERE
# if [ "$SKIP_MIGRATIONS" != "true" ]
#   then
#     echo "Syncing core database structure..."
#     # 1. Force migrate the public schema's core apps first without triggering tenant logic
#     python manage.py migrate --schema=public

#     echo "Running tenant database migrations..."
#     # 2. Run the actual tenant-safe migration command
#     python manage.py migrate_schemas --shared
#     python manage.py migrate_schemas --tenant
# fi

# echo "Collecting static files..."
python manage.py collectstatic --no-input

# This passes control to whatever command you run in docker-compose (like gunicorn)
exec "$@"
