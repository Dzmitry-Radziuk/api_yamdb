from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrModeratorOrAdmin(BasePermission):
    """
    Пермишен для проверки, является ли пользователь автором,
    модератором или администратором.
    """

    def has_permission(self, request, view):
        """Запрещаем неавторизованным пользователям `POST` и `PATCH`."""
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверяем права для конкретного объекта."""
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated and (
                request.user == obj.author or
                getattr(request.user, "role", None) in ["moderator", "admin"]
            )
        )