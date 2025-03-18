from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Разрешает доступ только администраторам."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'