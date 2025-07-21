from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer
from .serializers import CustomerSerializer, CustomerRegistrationSerializer, CustomerResponseSerializer

@api_view(['POST'])
def register_customer(request):
    """
    Register a new customer with approved limit based on monthly salary.
    """
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        response_serializer = CustomerResponseSerializer(customer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
