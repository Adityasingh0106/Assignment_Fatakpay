from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from .serializers import (
    TransactionSerializer,
    AddFundsSerializer,
    WalletSerializer
)
from .services import WalletService
from users.permissions import IsCustomer
from core.utils import create_success_response, create_error_response
from core.exceptions import InvalidTransactionError


class AddFundsView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def post(self, request):
        serializer = AddFundsSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                create_error_response(
                    message='Invalid data provided',
                    errors=serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            transaction_record = WalletService.credit_wallet(
                user=request.user,
                amount=serializer.validated_data['amount'],
                description=serializer.validated_data.get('description', 'Wallet credit')
            )
            
            wallet = WalletService.get_wallet(request.user)
            
            response_data = {
                'transaction': TransactionSerializer(transaction_record).data,
                'wallet': WalletSerializer(wallet).data
            }
            
            return Response(
                create_success_response(
                    message='Funds added successfully',
                    data=response_data
                ),
                status=status.HTTP_200_OK
            )
            
        except InvalidTransactionError as e:
            return Response(
                create_error_response(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                create_error_response(
                    message='Failed to add funds',
                    errors=str(e)
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def get_queryset(self):
        wallet = WalletService.get_or_create_wallet(self.request.user)
        return Transaction.objects.filter(wallet=wallet)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            create_success_response(
                message='Transaction history retrieved successfully',
                data=serializer.data
            )
        )


class WalletBalanceView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def get(self, request):
        balance = WalletService.get_wallet_balance(request.user)
        
        return Response(
            create_success_response(
                message='Balance retrieved successfully',
                data={'balance': str(balance)}
            )
        )
