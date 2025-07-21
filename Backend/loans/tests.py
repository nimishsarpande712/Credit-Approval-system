from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from decimal import Decimal
from datetime import timedelta
from .models import Loan
from customers.models import Customer
from .utils import calculate_monthly_installment, check_loan_eligibility

class LoanUtilsTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            customer_id=1,
            first_name="John",
            last_name="Doe",
            age=30,
            monthly_salary=50000,
            approved_limit=1800000,
            phone_number="9876543210"
        )
        
    def test_calculate_monthly_installment(self):
        """Test monthly installment calculation"""
        # Principal: 100000, Interest: 10%, Tenure: 12 months
        emi = calculate_monthly_installment(100000, 10, 12)
        self.assertAlmostEqual(emi, 8791.59, places=2)
    
    def test_check_loan_eligibility_approved(self):
        """Test loan eligibility check for approved loan"""
        # Create a past loan with good repayment history
        Loan.objects.create(
            loan_id=1,
            customer=self.customer,
            loan_amount=50000,
            tenure=12,
            interest_rate=10,
            monthly_repayment=4500,
            emis_paid_on_time=12,  # All EMIs paid on time
            start_date=timezone.now().date() - timedelta(days=365),
            end_date=timezone.now().date() - timedelta(days=30)
        )
        
        # Check eligibility for new loan
        approval, corrected_rate, emi = check_loan_eligibility(
            self.customer.customer_id, 100000, 10, 12
        )
        
        self.assertTrue(approval)
        self.assertEqual(corrected_rate, 10.0)
        self.assertGreater(emi, 0)

class LoanAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            customer_id=1,
            first_name="John",
            last_name="Doe",
            age=30,
            monthly_salary=50000,
            approved_limit=1800000,
            phone_number="9876543210"
        )
        
        # Create a loan for testing
        self.loan = Loan.objects.create(
            loan_id=1,
            customer=self.customer,
            loan_amount=100000,
            tenure=12,
            interest_rate=10,
            monthly_repayment=8791.59,
            emis_paid_on_time=3,
            start_date=timezone.now().date() - timedelta(days=90),
            end_date=timezone.now().date() + timedelta(days=270)
        )
    
    def test_view_loan(self):
        """Test viewing a loan"""
        response = self.client.get(f'/api/view-loan/{self.loan.loan_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['loan_id'], 1)
        self.assertEqual(response.data['customer']['first_name'], 'John')
        self.assertEqual(response.data['loan_amount'], '100000.00')
    
    def test_view_customer_loans(self):
        """Test viewing customer loans"""
        response = self.client.get(f'/api/view-loans/{self.customer.customer_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['loan_id'], 1)
        self.assertEqual(response.data[0]['repayments_left'], 9)  # 12 - 3 = 9
