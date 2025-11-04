from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    OrderDetailSerializer,
    CreatePurchaseSerializer,
)
from .services import PurchaseService
from wallet.serializers import TransactionSerializer
from users.permissions import IsCustomer
from core.utils import create_success_response, create_error_response
from core.exceptions import (
    InsufficientBalanceError,
    StockUnavailableError,
    ProductNotFoundError,
    InvalidTransactionError
)


class CreatePurchaseView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def post(self, request):
        serializer = CreatePurchaseSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                create_error_response(
                    message='Invalid purchase data',
                    errors=serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            purchase_result = PurchaseService.create_purchase(
                customer=request.user,
                product_id=serializer.validated_data['product_id'],
                quantity=serializer.validated_data['quantity']
            )
            
            response_data = {
                'order': OrderDetailSerializer(purchase_result['order']).data,
                'transaction': TransactionSerializer(purchase_result['transaction']).data,
                'total_amount': str(purchase_result['total_amount']),
                'remaining_balance': str(purchase_result['remaining_balance'])
            }
            
            return Response(
                create_success_response(
                    message='Purchase completed successfully',
                    data=response_data
                ),
                status=status.HTTP_201_CREATED
            )
            
        except ProductNotFoundError as e:
            return Response(
                create_error_response(str(e.detail)),
                status=status.HTTP_404_NOT_FOUND
            )
        except StockUnavailableError as e:
            return Response(
                create_error_response(
                    message='Insufficient stock',
                    errors=e.detail
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except InsufficientBalanceError as e:
            return Response(
                create_error_response(
                    message='Insufficient wallet balance',
                    errors=e.detail
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidTransactionError as e:
            return Response(
                create_error_response(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                create_error_response(
                    message='Purchase failed',
                    errors=str(e)
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
