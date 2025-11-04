from typing import Optional, List, Dict, Any
from decimal import Decimal
from django.db.models import QuerySet, Q
from .models import Product
from core.exceptions import ProductNotFoundError, StockUnavailableError


class ProductService:
    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ProductNotFoundError(f"Product with ID {product_id} not found.")
    
    @staticmethod
    def get_all_products(
        in_stock_only: bool = False,
        search: Optional[str] = None
    ) -> QuerySet[Product]:
        queryset = Product.objects.all()
        
        if in_stock_only:
            queryset = queryset.filter(stock_quantity__gt=0)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset
    
    @staticmethod
    def create_product(
        name: str,
        price: Decimal,
        stock_quantity: int,
        description: str = ''
    ) -> Product:
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity
        )
        return product
    
    @staticmethod
    def update_product(
        product_id: int,
        **update_fields
    ) -> Product:
        product = ProductService.get_product_by_id(product_id)
        
        for field, value in update_fields.items():
            if hasattr(product, field):
                setattr(product, field, value)
        
        product.save()
        return product
    
    @staticmethod
    def delete_product(product_id: int) -> None:
        product = ProductService.get_product_by_id(product_id)
        product.delete()
    
    @staticmethod
    def check_stock_availability(
        product_id: int,
        required_quantity: int
    ) -> tuple[bool, Optional[str]]:
        try:
            product = ProductService.get_product_by_id(product_id)
        except ProductNotFoundError as e:
            return False, str(e)
        
        if product.stock_quantity < required_quantity:
            return False, (
                f"Insufficient stock. Available: {product.stock_quantity}, "
                f"Required: {required_quantity}"
            )
        
        return True, None
    
    @staticmethod
    def update_stock(
        product_id: int,
        quantity_change: int,
        operation: str = 'reduce'
    ) -> Product:
        product = ProductService.get_product_by_id(product_id)
        
        if operation == 'reduce':
            if quantity_change > product.stock_quantity:
                raise StockUnavailableError(
                    product_name=product.name,
                    requested=quantity_change,
                    available=product.stock_quantity
                )
            product.reduce_stock(quantity_change)
        elif operation == 'increase':
            product.increase_stock(quantity_change)
        
        return product
    
    @staticmethod
    def bulk_create_or_update_products(
        products_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        created_count = 0
        updated_count = 0
        failed_count = 0
        errors = []
        
        for product_data in products_data:
            try:
                product, created = Product.objects.update_or_create(
                    name=product_data['name'],
                    defaults={
                        'description': product_data.get('description', ''),
                        'price': product_data['price'],
                        'stock_quantity': product_data['stock_quantity']
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
                    
            except Exception as e:
                failed_count += 1
                errors.append({
                    'product': product_data.get('name', 'Unknown'),
                    'error': str(e)
                })
        
        return {
            'created': created_count,
            'updated': updated_count,
            'failed': failed_count,
            'errors': errors
        }




