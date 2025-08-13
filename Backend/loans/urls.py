from django.urls import path
from . import views
from django.shortcuts import render
from django.urls import path

def home(request):
    return render(request, 'index.html')

urlpatterns = [
    path('', home),
]


urlpatterns = [
    path('check-eligibility/', views.check_eligibility, name='check-eligibility'),
    path('create-loan/', views.create_loan, name='create-loan'),
    path('view-loan/<int:loan_id>/', views.LoanDetailView.as_view(), name='view-loan'),
    path('view-loans/<int:customer_id>/', views.CustomerLoansView.as_view(), name='view-loans'),
]
