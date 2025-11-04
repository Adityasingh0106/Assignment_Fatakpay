"""
App configuration for wallet app.
"""
from django.apps import AppConfig


class WalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet'
    
    def ready(self):
        """Import signals when app is ready."""
        import wallet.signals
