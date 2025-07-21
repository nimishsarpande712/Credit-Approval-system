from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from customers.models import Customer
from .models import Loan
from .serializers import (
    LoanEligibilityRequestSerializer, 
    LoanEligibilityResponseSerializer,
    LoanCreateRequestSerializer,
    LoanCreateResponseSerializer,
    LoanDetailSerializer,
    CustomerLoansSerializer
)
from .utils import check_loan_eligibility, calculate_monthly_installment, calculate_credit_score
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta

@api_view(['POST'])
def check_eligibility(request):
    """
    Check loan eligibility based on customer's credit score.
    """
    serializer = LoanEligibilityRequestSerializer(data=request.data)
    if serializer.is_valid():
        customer_id = serializer.validated_data['customer_id']
        loan_amount = serializer.validated_data['loan_amount']
        interest_rate = serializer.validated_data['interest_rate']
        tenure = serializer.validated_data['tenure']
        
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check eligibility
        approval, corrected_interest_rate, monthly_installment = check_loan_eligibility(
            customer_id, loan_amount, interest_rate, tenure
        )
        
        response_data = {
            'customer_id': customer_id,
            'approval': approval,
            'interest_rate': interest_rate,
            'corrected_interest_rate': corrected_interest_rate,
            'tenure': tenure,
            'monthly_installment': monthly_installment
        }
        
        response_serializer = LoanEligibilityResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_loan(request):
    """
    Process a new loan based on eligibility.
    """
    serializer = LoanCreateRequestSerializer(data=request.data)
    if serializer.is_valid():
        customer_id = serializer.validated_data['customer_id']
        loan_amount = serializer.validated_data['loan_amount']
        interest_rate = serializer.validated_data['interest_rate']
        tenure = serializer.validated_data['tenure']
        
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check eligibility
        approval, corrected_interest_rate, monthly_installment = check_loan_eligibility(
            customer_id, loan_amount, interest_rate, tenure
        )
        
        if approval:
            # Create new loan
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=30*tenure)
            
            loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                interest_rate=corrected_interest_rate,
                tenure=tenure,
                monthly_repayment=monthly_installment,
                emis_paid_on_time=0,
                start_date=start_date,
                end_date=end_date
            )
            
            # Update customer's current debt
            customer.current_debt += float(loan_amount)
            customer.save()
            
            response_data = {
                'loan_id': loan.loan_id,
                'customer_id': customer_id,
                'loan_approved': True,
                'message': "Loan approved successfully",
                'monthly_installment': monthly_installment
            }
        else:
            response_data = {
                'loan_id': None,
                'customer_id': customer_id,
                'loan_approved': False,
                'message': "Loan not approved. Credit score too low or EMIs exceed 50% of salary.",
                'monthly_installment': monthly_installment
            }
        
        response_serializer = LoanCreateResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanDetailView(RetrieveAPIView):
    """
    View loan details and customer details.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanDetailSerializer
    lookup_url_kwarg = 'loan_id'

class CustomerLoansView(ListAPIView):
    """
    View all current loan details by customer id.
    """
    serializer_class = CustomerLoansSerializer
    
    def get_queryset(self):
        customer_id = self.kwargs.get('customer_id')
        # Get only active loans (end_date >= today)
        return Loan.objects.filter(
            customer__customer_id=customer_id,
            end_date__gte=timezone.now().date()
        )
