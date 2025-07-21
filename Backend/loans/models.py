from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import Customer

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, related_name='loans', on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    tenure = models.IntegerField(validators=[MinValueValidator(1)])
    interest_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    monthly_repayment = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"Loan {self.loan_id} - Customer {self.customer.customer_id}"
