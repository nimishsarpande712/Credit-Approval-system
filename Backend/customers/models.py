from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(18)])
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    approved_limit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    current_debt = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_id})"
    
    def calculate_approved_limit(self):
        # approved_limit = 36 * monthly_salary (rounded to nearest lakh)
        monthly_salary = float(self.monthly_salary)
        limit = 36 * monthly_salary
        # Round to nearest lakh (100,000)
        limit = round(limit / 100000) * 100000
        return limit
