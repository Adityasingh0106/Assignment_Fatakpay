from django.contrib import admin
from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'balance', 'has_sufficient_balance',
        'created_at', 'updated_at'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'has_sufficient_balance']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Balance', {
            'fields': ('balance', 'has_sufficient_balance')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_sufficient_balance(self, obj):
        return obj.has_sufficient_balance
    has_sufficient_balance.boolean = True
    has_sufficient_balance.short_description = 'Has Balance'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'wallet', 'transaction_type', 'amount',
        'balance_after_transaction', 'description', 'timestamp'
    ]
    list_filter = ['transaction_type', 'timestamp']
    search_fields = ['wallet__user__username', 'description']
    readonly_fields = [
        'wallet', 'transaction_type', 'amount',
        'balance_after_transaction', 'description', 'timestamp'
    ]
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('wallet', 'transaction_type', 'amount', 'description')
        }),
        ('Balance Information', {
            'fields': ('balance_after_transaction',)
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
