from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """Разрешение для администраторов."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin  #


class IsModerator(permissions.BasePermission):
    """Разрешение для модераторов."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class AdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем, запись — только администраторам.
    """

    def has_permission(self, request, view):
        """Разрешает GET-запросы для всех пользователей."""
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    """
    Разрешение для авторов, модераторов и администраторов.
    Разрешает чтение всем, а запись — только автору, модератору или админу.
    """

    def has_permission(self, request, view):
        """Разрешает GET-запросы для всех пользователей."""
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверяем права для конкретного объекта."""
        return request.method in SAFE_METHODS or (
            request.user == obj.author
            or request.user.is_admin
            or request.user.is_moderator
        )
