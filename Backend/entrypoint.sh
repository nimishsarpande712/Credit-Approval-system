#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "PostgreSQL started"

# Apply migrations
python manage.py migrate --noinput

# Create superuser if needed
python manage.py create_superuser_if_none_exists

# Load initial data using Celery tasks
python manage.py shell -c "from customers.tasks import load_customer_data; load_customer_data.delay()"
python manage.py shell -c "from loans.tasks import load_loan_data; load_loan_data.delay()"

# Start the Django application
python manage.py runserver 0.0.0.0:8000
