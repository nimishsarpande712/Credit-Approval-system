from celery import shared_task
import pandas as pd
from .models import Loan
from customers.models import Customer
from datetime import datetime
import os

@shared_task
def load_loan_data():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'loan_data.xlsx')
    
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}
    
    # Load loan data from Excel file
    df = pd.read_excel(file_path)
    
    # Process each row in the dataframe
    for _, row in df.iterrows():
        # Check if customer exists
        try:
            customer = Customer.objects.get(customer_id=row['customer_id'])
            
            # Check if loan already exists
            if not Loan.objects.filter(loan_id=row['loan_id']).exists():
                # Convert date format if needed
                start_date = row['start_date']
                end_date = row['end_date']
                
                if not isinstance(start_date, datetime):
                    start_date = datetime.strptime(str(start_date), "%Y-%m-%d")
                    
                if not isinstance(end_date, datetime):
                    end_date = datetime.strptime(str(end_date), "%Y-%m-%d")
                
                Loan.objects.create(
                    loan_id=row['loan_id'],
                    customer=customer,
                    loan_amount=row['loan_amount'],
                    tenure=row['tenure'],
                    interest_rate=row['interest_rate'],
                    monthly_repayment=row['monthly_repayment'],
                    emis_paid_on_time=row['EMIs paid on time'],
                    start_date=start_date,
                    end_date=end_date
                )
        except Customer.DoesNotExist:
            # Skip this record if customer doesn't exist
            continue
    
    return {"status": "success", "message": f"Processed {len(df)} loan records"}
