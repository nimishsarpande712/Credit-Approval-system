#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
while ! nc -z $DB_HOST 5432; do
  sleep 0.5
done
echo "PostgreSQL started"

# Apply migrations
python manage.py migrate --noinput

# Optional: Create superuser if needed
python manage.py create_superuser_if_none_exists || true

# Start the Django application with Gunicorn
exec gunicorn credit_approval_system.wsgi:application --bind 0.0.0.0:8000
