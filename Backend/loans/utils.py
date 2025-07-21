from decimal import Decimal
from customers.models import Customer
from loans.models import Loan
from django.utils import timezone
import math

def calculate_credit_score(customer_id):
    """
    Calculate credit score for a customer based on various factors.
    
    Components:
    1. Past Loans paid on time
    2. No of loans taken in past
    3. Loan activity in current year
    4. Loan approved volume
    5. If sum of current loans > approved limit, credit score = 0
    
    Returns a score from 0 to 100
    """
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return 0
    
    # Get all loans for the customer
    loans = Loan.objects.filter(customer=customer)
    
    if not loans.exists():
        # No loan history, give a default moderate score
        return 50
    
    # Component 1: Past loans paid on time (30 points)
    total_emis = sum(loan.tenure for loan in loans)
    emis_paid_on_time = sum(loan.emis_paid_on_time for loan in loans)
    
    if total_emis > 0:
        on_time_ratio = emis_paid_on_time / total_emis
        on_time_score = min(30, int(on_time_ratio * 30))
    else:
        on_time_score = 15  # Default middle value
    
    # Component 2: Number of loans taken in past (20 points)
    # Fewer loans is generally better for credit score
    num_loans = loans.count()
    if num_loans <= 2:
        num_loans_score = 20
    elif num_loans <= 5:
        num_loans_score = 15
    elif num_loans <= 10:
        num_loans_score = 10
    else:
        num_loans_score = 5
    
    # Component 3: Loan activity in current year (20 points)
    current_year = timezone.now().year
    loans_this_year = loans.filter(start_date__year=current_year).count()
    
    if loans_this_year == 0:
        current_activity_score = 20
    elif loans_this_year == 1:
        current_activity_score = 15
    elif loans_this_year <= 3:
        current_activity_score = 10
    else:
        current_activity_score = 5
    
    # Component 4: Loan approved volume (30 points)
    # Lower volume compared to limit is better
    total_loan_amount = sum(float(loan.loan_amount) for loan in loans)
    approved_limit = float(customer.approved_limit)
    
    if approved_limit > 0:
        volume_ratio = total_loan_amount / approved_limit
        if volume_ratio <= 0.3:
            volume_score = 30
        elif volume_ratio <= 0.5:
            volume_score = 25
        elif volume_ratio <= 0.7:
            volume_score = 20
        elif volume_ratio <= 0.9:
            volume_score = 10
        else:
            volume_score = 5
    else:
        volume_score = 0
    
    # Component 5: If sum of current loans > approved limit, score = 0
    current_loans = loans.filter(end_date__gte=timezone.now().date())
    current_loan_amount = sum(float(loan.loan_amount) for loan in current_loans)
    
    if current_loan_amount > approved_limit:
        return 0
    
    # Calculate final score
    credit_score = on_time_score + num_loans_score + current_activity_score + volume_score
    
    return min(100, credit_score)  # Cap at 100

def calculate_monthly_installment(principal, interest_rate, tenure):
    """
    Calculate the monthly installment amount using compound interest.
    
    Args:
        principal: Loan amount
        interest_rate: Annual interest rate (in percentage)
        tenure: Loan duration in months
    
    Returns:
        Monthly installment amount
    """
    # Convert annual interest rate to monthly rate (decimal)
    r = float(interest_rate) / (12 * 100)
    
    # Calculate monthly installment using compound interest formula
    emi = float(principal) * r * (1 + r) ** tenure / ((1 + r) ** tenure - 1)
    
    return round(emi, 2)

def check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure):
    """
    Check if a customer is eligible for a loan.
    
    Returns:
        tuple: (is_approved, corrected_interest_rate, monthly_installment)
    """
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return False, interest_rate, 0
    
    # Get credit score
    credit_score = calculate_credit_score(customer_id)
    
    # Check if monthly EMIs exceed 50% of monthly salary
    current_loans = Loan.objects.filter(
        customer=customer,
        end_date__gte=timezone.now().date()
    )
    
    total_monthly_emi = sum(float(loan.monthly_repayment) for loan in current_loans)
    new_emi = calculate_monthly_installment(loan_amount, interest_rate, tenure)
    total_emi_with_new_loan = total_monthly_emi + new_emi
    
    # If EMIs exceed 50% of salary, reject
    if total_emi_with_new_loan > (float(customer.monthly_salary) * 0.5):
        return False, interest_rate, new_emi
    
    # Apply credit score rules
    if credit_score > 50:
        # Approve loan
        return True, interest_rate, new_emi
    elif 30 < credit_score <= 50:
        # Approve with minimum 12% interest rate
        corrected_rate = max(float(interest_rate), 12.0)
        if corrected_rate != float(interest_rate):
            new_emi = calculate_monthly_installment(loan_amount, corrected_rate, tenure)
        return True, corrected_rate, new_emi
    elif 10 < credit_score <= 30:
        # Approve with minimum 16% interest rate
        corrected_rate = max(float(interest_rate), 16.0)
        if corrected_rate != float(interest_rate):
            new_emi = calculate_monthly_installment(loan_amount, corrected_rate, tenure)
        return True, corrected_rate, new_emi
    else:
        # Reject for credit score <= 10
        return False, interest_rate, new_emi
