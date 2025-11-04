from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import QuerySet

from .models import Product
from .serializers import (
    ProductSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductUpdateSerializer
)
from .services import ProductService
from users.permissions import IsAdmin, IsAdminOrReadOnly
from core.utils import create_success_response, create_error_response
from core.exceptions import ProductNotFoundError


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductSerializer
        return ProductListSerializer
    
    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            create_success_response(
                message='Products retrieved successfully',
                data=serializer.data
            )
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = ProductService.create_product(
            name=serializer.validated_data['name'],
            description=serializer.validated_data.get('description', ''),
            price=serializer.validated_data['price'],
            stock_quantity=serializer.validated_data['stock_quantity']
        )
        
        response_serializer = ProductDetailSerializer(product)
        return Response(
            create_success_response(
                message='Product created successfully',
                data=response_serializer.data
            ),
            status=status.HTTP_201_CREATED
        )


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductUpdateSerializer
        return ProductDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            return Response(
                create_success_response(
                    message='Product retrieved successfully',
                    data=serializer.data
                )
            )
        except Product.DoesNotExist:
            return Response(
                create_error_response('Product not found'),
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        updated_product = ProductService.update_product(
            product_id=instance.id,
            **serializer.validated_data
        )
        
        response_serializer = ProductDetailSerializer(updated_product)
        return Response(
            create_success_response(
                message='Product updated successfully',
                data=response_serializer.data
            )
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ProductService.delete_product(instance.id)
        
        return Response(
            create_success_response(
                message='Product deleted successfully'
            ),
            status=status.HTTP_200_OK
        )
