from rest_framework import serializers
from .models import Wallet, Transaction
from core.validators import validate_positive_amount


class WalletSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    has_sufficient_balance = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Wallet
        fields = [
            'id', 'username', 'balance', 'has_sufficient_balance',
            'created_at', 'updated_at'
        ]
        read_only_fields = fields


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type_display = serializers.CharField(
        source='get_transaction_type_display',
        read_only=True
    )
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'transaction_type_display',
            'amount', 'balance_after_transaction', 'description', 'timestamp'
        ]
        read_only_fields = fields


class AddFundsSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )
    description = serializers.CharField(
        max_length=255,
        required=False,
        default='Wallet credit'
    )
    
    def validate_amount(self, value):
        return validate_positive_amount(value)


class TransactionFilterSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(
        choices=Transaction.TransactionType.choices,
        required=False
    )
    limit = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=100
    )




