from rest_framework import serializers
from .models import Loan
from customers.models import Customer
from customers.serializers import CustomerSerializer
from decimal import Decimal
import math

class LoanEligibilityRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()

class LoanEligibilityResponseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    approval = serializers.BooleanField()
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    corrected_interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)

class LoanCreateRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()

class LoanCreateResponseSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField(allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField(allow_blank=True)
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)

class CustomerLoanDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='customer_id')
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    age = serializers.IntegerField()

class LoanDetailSerializer(serializers.ModelSerializer):
    customer = CustomerLoanDetailSerializer()
    
    class Meta:
        model = Loan
        fields = ('loan_id', 'customer', 'loan_amount', 'interest_rate', 'monthly_repayment', 'tenure')

class CustomerLoansSerializer(serializers.ModelSerializer):
    repayments_left = serializers.SerializerMethodField()
    
    class Meta:
        model = Loan
        fields = ('loan_id', 'loan_amount', 'interest_rate', 'monthly_repayment', 'repayments_left')
    
    def get_repayments_left(self, obj):
        return obj.tenure - obj.emis_paid_on_time
