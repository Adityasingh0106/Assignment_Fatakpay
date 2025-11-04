from rest_framework.exceptions import APIException
from rest_framework import status


class InsufficientBalanceError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Insufficient wallet balance for this transaction.'
    default_code = 'insufficient_balance'

    def __init__(self, required_balance: float, available_balance: float):
        self.detail = {
            'error': 'Insufficient wallet balance',
            'required_balance': required_balance,
            'available_balance': available_balance,
            'shortfall': required_balance - available_balance
        }


class StockUnavailableError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Insufficient product stock available.'
    default_code = 'stock_unavailable'

    def __init__(self, product_name: str, requested: int, available: int):
        self.detail = {
            'error': 'Insufficient stock',
            'product': product_name,
            'requested_quantity': requested,
            'available_quantity': available
        }


class InvalidTransactionError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid transaction.'
    default_code = 'invalid_transaction'


class ProductNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Product not found.'
    default_code = 'product_not_found'


class WalletNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Wallet not found for this user.'
    default_code = 'wallet_not_found'


class UnauthorizedAccessError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'unauthorized_access'




