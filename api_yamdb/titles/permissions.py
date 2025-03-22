from rest_framework import permissions


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
