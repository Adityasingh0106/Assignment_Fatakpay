from typing import Dict, Any
from decimal import Decimal
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Order
from products.models import Product
from products.services import ProductService
from wallet.services import WalletService
from core.exceptions import (
    InsufficientBalanceError,
    StockUnavailableError,
    ProductNotFoundError,
    InvalidTransactionError
)

User = get_user_model()


class PurchaseService:
    @staticmethod
    @transaction.atomic
    def create_purchase(
        customer: User,
        product_id: int,
        quantity: int
    ) -> Dict[str, Any]:
        if quantity <= 0:
            raise InvalidTransactionError("Quantity must be greater than zero")
        
        try:
            product = Product.objects.select_for_update().get(id=product_id)
        except Product.DoesNotExist:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        if product.stock_quantity < quantity:
            raise StockUnavailableError(
                product_name=product.name,
                requested=quantity,
                available=product.stock_quantity
            )
        
        total_cost = product.price * quantity
        
        if not WalletService.check_sufficient_balance(customer, total_cost):
            wallet_balance = WalletService.get_wallet_balance(customer)
            raise InsufficientBalanceError(
                required_balance=float(total_cost),
                available_balance=float(wallet_balance)
            )
        
        transaction_record = WalletService.debit_wallet(
            user=customer,
            amount=total_cost,
            description=f"Purchase: {product.name} x{quantity}"
        )
        
        product.reduce_stock(quantity)
        
        order = Order.objects.create(
            customer=customer,
            product=product,
            quantity=quantity,
            unit_price=product.price,
            total_price=total_cost,
            status=Order.OrderStatus.COMPLETED
        )
        
        return {
            'order': order,
            'transaction': transaction_record,
            'product': product,
            'total_amount': total_cost,
            'remaining_balance': WalletService.get_wallet_balance(customer)
        }
    
    @staticmethod
    def get_customer_orders(
        customer: User,
        status: str = None
    ):
        queryset = Order.objects.filter(customer=customer).select_related('product')
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    @staticmethod
    def get_order_by_id(order_id: int, customer: User = None) -> Order:
        queryset = Order.objects.select_related('product', 'customer')
        
        if customer:
            queryset = queryset.filter(customer=customer)
        
        return queryset.get(id=order_id)
    
    @staticmethod
    def get_order_statistics(customer: User) -> Dict[str, Any]:
        orders = Order.objects.filter(customer=customer)
        
        total_orders = orders.count()
        total_spent = sum(order.total_price for order in orders)
        completed_orders = orders.filter(status=Order.OrderStatus.COMPLETED).count()
        
        return {
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'total_spent': total_spent
        }




