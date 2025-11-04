from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer', 'product', 'quantity',
        'unit_price', 'total_price', 'status', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = [
        'customer__username', 'customer__email',
        'product__name'
    ]
    readonly_fields = [
        'customer', 'product', 'quantity', 'unit_price',
        'total_price', 'created_at'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer',)
        }),
        ('Product Information', {
            'fields': ('product', 'quantity')
        }),
        ('Pricing', {
            'fields': ('unit_price', 'total_price')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
