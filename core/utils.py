from typing import Dict, Any
from decimal import Decimal


def format_currency(amount: float | Decimal) -> str:
    return f"₹{Decimal(str(amount)):.2f}"


def create_success_response(message: str, data: Any = None) -> Dict[str, Any]:
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return response


def create_error_response(message: str, errors: Any = None) -> Dict[str, Any]:
    response = {
        'success': False,
        'message': message
    }
    if errors is not None:
        response['errors'] = errors
    return response


def calculate_percentage(part: float | Decimal, whole: float | Decimal) -> Decimal:
    if whole == 0:
        return Decimal('0')
    return (Decimal(str(part)) / Decimal(str(whole))) * 100




