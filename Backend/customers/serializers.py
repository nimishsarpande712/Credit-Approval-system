from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 'first_name', 'last_name', 'age', 'monthly_salary', 'approved_limit', 'phone_number')

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'age', 'monthly_salary', 'phone_number')
    
    def create(self, validated_data):
        # Get the max customer_id and increment by 1
        max_id = Customer.objects.order_by('-customer_id').first()
        next_id = (max_id.customer_id + 1) if max_id else 1
        
        customer = Customer(
            customer_id=next_id,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data['age'],
            monthly_salary=validated_data['monthly_salary'],
            phone_number=validated_data['phone_number']
        )
        # Calculate approved limit based on monthly salary
        customer.approved_limit = customer.calculate_approved_limit()
        customer.save()
        return customer

class CustomerResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    monthly_income = serializers.DecimalField(source='monthly_salary', max_digits=12, decimal_places=2)
    
    class Meta:
        model = Customer
        fields = ('customer_id', 'name', 'age', 'monthly_income', 'approved_limit', 'phone_number')
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
