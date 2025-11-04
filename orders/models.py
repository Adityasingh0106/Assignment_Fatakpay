from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        PENDING = 'PENDING', 'Pending'
    
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.COMPLETED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self) -> str:
        return (
            f"Order #{self.id} - {self.customer.username} - "
            f"{self.product.name} x{self.quantity}"
        )
    
    @property
    def total_amount(self) -> Decimal:
        return self.unit_price * self.quantity
