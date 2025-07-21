from celery import shared_task
import pandas as pd
from .models import Customer
from loans.models import Loan
from datetime import datetime
import os

@shared_task
def load_customer_data():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'customer_data.xlsx')
    
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}
    
    # Load customer data from Excel file
    df = pd.read_excel(file_path)
    
    # Process each row in the dataframe
    for _, row in df.iterrows():
        # Check if customer already exists
        if not Customer.objects.filter(customer_id=row['customer_id']).exists():
            Customer.objects.create(
                customer_id=row['customer_id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                phone_number=row['phone_number'],
                monthly_salary=row['monthly_salary'],
                approved_limit=row['approved_limit'],
                current_debt=row['current_debt'] if 'current_debt' in row else 0,
                age=30  # Default age since it's not in the provided data
            )
    
    return {"status": "success", "message": f"Processed {len(df)} customer records"}
