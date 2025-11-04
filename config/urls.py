
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce Backend API",
        default_version='v1',
        description="""
        E-commerce Backend REST API
        
        Features:
        - JWT Authentication
        - User Management (Admin & Customer roles)
        - Product Management
        - Wallet System with Transactions
        - Purchase Flow with Atomic Operations
        
        Authentication:
        Use Bearer token: Authorization: Bearer <access_token>
        """,
        contact=openapi.Contact(email="contact@ecommerce.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api-redoc'),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/wallet/', include('wallet.urls')),
    path('api/orders/', include('orders.urls')),
]
