from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN
    
    @property
    def is_customer(self) -> bool:
        return self.role == self.Role.CUSTOMER
    
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.username
