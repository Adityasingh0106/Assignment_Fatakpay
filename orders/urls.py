from django.urls import path
from .views import (
    CreatePurchaseView,
)

app_name = 'orders'

urlpatterns = [
    path('purchase/', CreatePurchaseView.as_view(), name='create_purchase'),
]


