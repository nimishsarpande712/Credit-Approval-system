# Credit Approval System

A Django-based credit approval system that processes customer registrations, evaluates loan eligibility based on customer credit scores, and manages loan applications.

## Features

- Customer registration with automatic credit limit calculation
- Loan eligibility check based on credit score and other factors
- Loan creation with validation
- View loan details
- View customer loans

## Technology Stack

- Backend:
  - Django 4.x with Django Rest Framework
  - PostgreSQL for database
  - Celery for background tasks
  - Redis as message broker
  
- Frontend:
  - Simple HTML/Bootstrap interface

## API Endpoints

- `/api/register/` - Register a new customer
- `/api/check-eligibility/` - Check loan eligibility
- `/api/create-loan/` - Create a new loan
- `/api/view-loan/{loan_id}/` - View loan details
- `/api/view-loans/{customer_id}/` - View all loans for a customer

## Setup Instructions

### Using Docker Compose

1. Clone the repository:
```
git clone https://github.com/nimishsarpande712/Credit-Approval-system.git
cd Credit-Approval-system
```

2. Start the application using Docker Compose:
```
docker-compose up
```

The application will be available at:
- Frontend: http://localhost
- API: http://localhost/api
- Admin Interface: http://localhost/admin (username: admin, password: admin123)

### Without Docker

1. Install dependencies:
```
cd Backend
pip install -r requirements.txt
```

2. Configure PostgreSQL database in settings.py

3. Run migrations:
```
python manage.py migrate
```

4. Create superuser:
```
python manage.py createsuperuser
```

5. Run Celery worker:
```
celery -A credit_approval worker --loglevel=info
```

6. Start the Django development server:
```
python manage.py runserver
```

## Data Import

The system automatically imports customer and loan data from Excel files (`customer_data.xlsx` and `loan_data.xlsx`) using Celery background tasks when the application starts.

## Credit Score Calculation

The system calculates credit scores based on multiple factors:
- Past loans paid on time
- Number of loans taken in the past
- Loan activity in the current year
- Loan approved volume
- Current debt vs approved limit