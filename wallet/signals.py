from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Wallet

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet_for_customer(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'role'):
        from users.models import User as UserModel
        
        if instance.role == UserModel.Role.CUSTOMER:
            Wallet.objects.get_or_create(user=instance)




