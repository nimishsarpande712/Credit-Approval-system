from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'customer', 'loan_amount', 'tenure', 'interest_rate', 'monthly_repayment', 'start_date', 'end_date')
    search_fields = ('loan_id', 'customer__first_name', 'customer__last_name')
    list_filter = ('interest_rate', 'start_date', 'end_date')
