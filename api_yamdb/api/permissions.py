from rest_framework import permissions



class IsAdmin(permissions.BasePermission):
    """Разрешение для администраторов."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsModerator(permissions.BasePermission):
    """Разрешение для модераторов."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

class IsUser(permissions.BasePermission):
    """Разрешение для аутентифицированных пользователей."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_user

class IsUserOrAdminOrModerator(permissions.BasePermission):
    """Разрешение для обычных пользователей, модераторов и администраторов."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_moderator
            or (hasattr(obj, "user") and request.user == obj.user)
        )
    
class AdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем, запись — только администраторам.

    Доступ к безопасным методам (GET) открыт для всех пользователей.
    Для методов записи (POST, PATCH, DELETE) требуется аутентификация
    и права администратора.
    """
    def has_permission(self, request, view):
        """Проверяет права доступа для запроса."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

