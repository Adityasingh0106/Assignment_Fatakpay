from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Only administrators can perform this action.'
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'is_admin') and
            request.user.is_admin
        )


class IsCustomer(permissions.BasePermission):
    message = 'Only customers can perform this action.'
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'is_customer') and
            request.user.is_customer
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    message = 'You can only access your own resources.'
    
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'is_admin') and request.user.is_admin:
            return True
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'is_admin') and
            request.user.is_admin
        )




