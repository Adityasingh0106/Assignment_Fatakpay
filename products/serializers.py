from rest_framework import serializers
from .models import Product
from core.validators import validate_positive_amount, validate_stock_quantity, validate_product_name


class ProductSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.BooleanField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock_quantity',
            'is_in_stock', 'is_low_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_in_stock', 'is_low_stock']
    
    def validate_name(self, value: str) -> str:
        return validate_product_name(value)
    
    def validate_price(self, value) -> any:
        return validate_positive_amount(value)
    
    def validate_stock_quantity(self, value) -> any:
        return validate_stock_quantity(value)
    
    def validate(self, attrs):
        if not self.instance:
            name = attrs.get('name', '').strip()
            if Product.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError({
                    'name': 'A product with this name already exists.'
                })
        
        if self.instance:
            name = attrs.get('name', self.instance.name).strip()
            if Product.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError({
                    'name': 'A product with this name already exists.'
                })
        
        return attrs


class ProductListSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'stock_quantity',
            'is_in_stock', 'created_at'
        ]
        read_only_fields = fields


class ProductDetailSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.BooleanField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock_quantity',
            'is_in_stock', 'is_low_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity']
    
    def validate_name(self, value: str) -> str:
        return validate_product_name(value)
    
    def validate_price(self, value) -> any:
        return validate_positive_amount(value)
    
    def validate_stock_quantity(self, value) -> any:
        return validate_stock_quantity(value)




