from rest_framework import permissions


# Custom permission for book management (admin only)
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: read-only for everyone, write for admins only
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission: owners can view their own data, admins can view all
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.user == request.user