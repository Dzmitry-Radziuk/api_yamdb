from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Разрешение для администраторов."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin()


class IsModerator(BasePermission):
    """Разрешение для модераторов."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moderator()


class IsUser(BasePermission):
    """Разрешение для аутентифицированных пользователей."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_user()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_user()


class IsUserOrAdminOrModerator(BasePermission):
    """Разрешение для обычных пользователей, модераторов и администраторов."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin()
                or request.user.is_moderator()
                or request.user == obj
            )
        )
