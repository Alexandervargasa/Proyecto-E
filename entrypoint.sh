#!/bin/sh
# entrypoint for Docker image: run migrations, collectstatic and start gunicorn
set -e

# Wait for DB here if using an external DB (optional)
# e.g., you can add a small loop to wait for Postgres before migrating

echo "=> Waiting for database (if any)"
python wait_for_db.py || true

# Apply DB migrations
echo "=> Applying database migrations"
python manage.py migrate --noinput

# Collect static files
echo "=> Collecting static files"
python manage.py collectstatic --noinput

# If a fixture is present and we haven't loaded data yet, you can loaddata here
# e.g., python manage.py loaddata data.json

echo "=> Starting Gunicorn"
exec gunicorn DjangoProject5.wsgi:application --bind 0.0.0.0:8000 --workers 3 --log-level info
