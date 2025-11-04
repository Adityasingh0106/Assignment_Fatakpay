from typing import Optional
from decimal import Decimal
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Wallet, Transaction
from core.exceptions import (
    InsufficientBalanceError,
    WalletNotFoundError,
    InvalidTransactionError
)

User = get_user_model()


class WalletService:
    @staticmethod
    def get_or_create_wallet(user: User) -> Wallet:
        wallet, created = Wallet.objects.get_or_create(
            user=user,
            defaults={'balance': Decimal('0.00')}
        )
        return wallet
    
    @staticmethod
    def get_wallet(user: User) -> Wallet:
        try:
            return Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            raise WalletNotFoundError(f"Wallet not found for user {user.username}")
    
    @staticmethod
    @transaction.atomic
    def credit_wallet(
        user: User,
        amount: Decimal,
        description: str = "Wallet credit"
    ) -> Transaction:
        if amount <= 0:
            raise InvalidTransactionError("Credit amount must be greater than zero")
        
        wallet = WalletService.get_or_create_wallet(user)
        wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
        
        wallet.balance += amount
        wallet.save(update_fields=['balance', 'updated_at'])
        
        transaction_record = Transaction.objects.create(
            wallet=wallet,
            transaction_type=Transaction.TransactionType.CREDIT,
            amount=amount,
            balance_after_transaction=wallet.balance,
            description=description
        )
        
        return transaction_record
    
    @staticmethod
    @transaction.atomic
    def debit_wallet(
        user: User,
        amount: Decimal,
        description: str = "Wallet debit"
    ) -> Transaction:
        if amount <= 0:
            raise InvalidTransactionError("Debit amount must be greater than zero")
        
        wallet = WalletService.get_wallet(user)
        wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
        
        if wallet.balance < amount:
            raise InsufficientBalanceError(
                required_balance=float(amount),
                available_balance=float(wallet.balance)
            )
        
        wallet.balance -= amount
        wallet.save(update_fields=['balance', 'updated_at'])
        
        transaction_record = Transaction.objects.create(
            wallet=wallet,
            transaction_type=Transaction.TransactionType.DEBIT,
            amount=amount,
            balance_after_transaction=wallet.balance,
            description=description
        )
        
        return transaction_record
    
    @staticmethod
    def get_wallet_balance(user: User) -> Decimal:
        wallet = WalletService.get_or_create_wallet(user)
        return wallet.balance
    
    @staticmethod
    def get_transaction_history(
        user: User,
        transaction_type: Optional[str] = None,
        limit: Optional[int] = None
    ):
        wallet = WalletService.get_or_create_wallet(user)
        queryset = Transaction.objects.filter(wallet=wallet)
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        if limit:
            queryset = queryset[:limit]
        
        return queryset
    
    @staticmethod
    def check_sufficient_balance(user: User, required_amount: Decimal) -> bool:
        try:
            wallet = WalletService.get_wallet(user)
            return wallet.balance >= required_amount
        except WalletNotFoundError:
            return False




