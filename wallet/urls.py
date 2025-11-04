from django.urls import path
from .views import (
    AddFundsView,
    TransactionHistoryView,
    WalletBalanceView
)

app_name = 'wallet'

urlpatterns = [
    path('balance/', WalletBalanceView.as_view(), name='wallet_balance'),
    path('add-funds/', AddFundsView.as_view(), name='add_funds'),
    path('transactions/', TransactionHistoryView.as_view(), name='transaction_history'),
]


