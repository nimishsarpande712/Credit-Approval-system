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
    try:
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            response_serializer = CustomerResponseSerializer(customer)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_messages = {}
            for field, errors in serializer.errors.items():
                error_messages[field] = str(errors[0]) if errors else "Invalid data"
            return Response({"error": error_messages}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
