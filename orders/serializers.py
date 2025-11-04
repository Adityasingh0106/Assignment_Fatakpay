from rest_framework import serializers
from .models import Order
from products.serializers import ProductListSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    product_details = ProductListSerializer(source='product', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_username', 'customer_email',
            'product', 'product_details', 'quantity',
            'unit_price', 'total_price', 'status', 'status_display',
            'created_at'
        ]
        read_only_fields = fields


class CreatePurchaseSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True, min_value=1)
    quantity = serializers.IntegerField(required=True, min_value=1)
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        if value > 1000:
            raise serializers.ValidationError("Quantity cannot exceed 1000 items per order")
        return value




