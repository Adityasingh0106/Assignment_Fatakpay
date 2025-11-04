from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} - ₹{self.price}"
    
    @property
    def is_in_stock(self) -> bool:
        return self.stock_quantity > 0
    
    @property
    def is_low_stock(self) -> bool:
        return 0 < self.stock_quantity < 10
    
    def reduce_stock(self, quantity: int) -> None:
        if quantity > self.stock_quantity:
            raise ValueError(
                f"Cannot reduce stock by {quantity}. "
                f"Only {self.stock_quantity} items available."
            )
        self.stock_quantity -= quantity
        self.save(update_fields=['stock_quantity', 'updated_at'])
    
    def increase_stock(self, quantity: int) -> None:
        self.stock_quantity += quantity
        self.save(update_fields=['stock_quantity', 'updated_at'])
