from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermissions):
    """
    Разрешает доступ всем для операций чтения (GET),
    и только администраторам для записи (POST, PATCH, DELETE).
    """
    def has_permission(self, request, view):
        if request.vethod in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'
