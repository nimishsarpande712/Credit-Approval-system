import pandas as pd
from django.core.management.base import BaseCommand
from customers.models import Customer
from loans.models import Loan
from decimal import Decimal

class Command(BaseCommand):
    help = 'Import data from Excel files'

    def handle(self, *args, **kwargs):
        # Import Customer Data
        try:
            customer_df = pd.read_excel('customer_data.xlsx')
            self.stdout.write('Importing customer data...')
            
            for _, row in customer_df.iterrows():
                customer, created = Customer.objects.update_or_create(
                    customer_id=row['Customer ID'],
                    defaults={
                        'first_name': row['First Name'],
                        'last_name': row['Last Name'],
                        'age': row['Age'],
                        'phone_number': str(row['Phone Number']),
                        'monthly_salary': Decimal(str(row['Monthly Salary'])),
                        'approved_limit': Decimal(str(row['Approved Limit']))
                    }
                )
                if created:
                    self.stdout.write(f'Created customer: {customer.first_name} {customer.last_name}')
                else:
                    self.stdout.write(f'Updated customer: {customer.first_name} {customer.last_name}')

            self.stdout.write(self.style.SUCCESS('Successfully imported customer data'))

            # Import Loan Data
            loan_df = pd.read_excel('loan_data.xlsx')
            self.stdout.write('Importing loan data...')
            
            for _, row in loan_df.iterrows():
                try:
                    customer = Customer.objects.get(customer_id=row['Customer ID'])
                    loan, created = Loan.objects.update_or_create(
                        loan_id=row['Loan ID'],
                        defaults={
                            'customer': customer,
                            'loan_amount': Decimal(str(row['Loan Amount'])),
                            'tenure': row['Tenure'],
                            'interest_rate': Decimal(str(row['Interest Rate'])),
                            'monthly_repayment': Decimal(str(row['Monthly payment'])),
                            'emis_paid_on_time': row['EMIs paid on Time'],
                            'start_date': pd.to_datetime(row['Date of Approval']).date(),
                            'end_date': pd.to_datetime(row['End Date']).date()
                        }
                    )
                    self.stdout.write(f'Created loan: {loan.loan_id} for customer {customer.customer_id}')
                except Customer.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Customer {row["Customer ID"]} does not exist, skipping loan {row["Loan ID"]}'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Error creating loan {row["Loan ID"]}: {str(e)}'
                    ))

            self.stdout.write(self.style.SUCCESS('Successfully imported loan data'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))
