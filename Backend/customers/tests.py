from django.test import TestCase
from rest_framework.test import APIClient
from .models import Customer
from decimal import Decimal

class CustomerModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            monthly_salary=50000,
            phone_number="9876543210"
        )
    
    def test_calculate_approved_limit(self):
        """Test the approved limit calculation"""
        # 36 * 50000 = 1800000, rounded to nearest lakh = 1800000
        self.customer.approved_limit = self.customer.calculate_approved_limit()
        self.customer.save()
        self.assertEqual(self.customer.approved_limit, Decimal('1800000'))

class CustomerRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_register_customer(self):
        """Test customer registration endpoint"""
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "age": 28,
            "monthly_salary": 60000,
            "phone_number": "9876543211"
        }
        
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Jane Smith')
        self.assertEqual(response.data['monthly_income'], '60000.00')
        # 36 * 60000 = 2160000, rounded to nearest lakh = 2200000
        self.assertEqual(response.data['approved_limit'], '2200000.00')
