from typing import Any
from decimal import Decimal
from rest_framework.serializers import ValidationError


def validate_positive_amount(value: Any) -> Any:
    if value is None:
        raise ValidationError("Amount cannot be null.")
    
    try:
        decimal_value = Decimal(str(value))
        if decimal_value <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return value
    except (ValueError, TypeError):
        raise ValidationError("Amount must be a valid number.")


def validate_stock_quantity(value: Any) -> Any:
    if value is None:
        raise ValidationError("Stock quantity cannot be null.")
    
    try:
        int_value = int(value)
        if int_value < 0:
            raise ValidationError("Stock quantity cannot be negative.")
        return value
    except (ValueError, TypeError):
        raise ValidationError("Stock quantity must be a valid integer.")


def validate_price(value: Any) -> Any:
    if value is None:
        raise ValidationError("Price cannot be null.")
    
    try:
        decimal_value = Decimal(str(value))
        if decimal_value <= 0:
            raise ValidationError("Price must be greater than zero.")
        
        if decimal_value.as_tuple().exponent < -2:
            raise ValidationError("Price cannot have more than 2 decimal places.")
        
        return value
    except (ValueError, TypeError):
        raise ValidationError("Price must be a valid number.")


def validate_product_name(value: str) -> str:
    if not value or not value.strip():
        raise ValidationError("Product name cannot be empty.")
    
    if len(value) > 255:
        raise ValidationError("Product name cannot exceed 255 characters.")
    
    return value.strip()




