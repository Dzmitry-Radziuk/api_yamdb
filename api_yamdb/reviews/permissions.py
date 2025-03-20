from rest_framework.permissions import BasePermission

class IsAuthorOrModeratorOrAdmin(BasePermission):
    """
    Пермишен для проверки, является ли пользователь автором,
    модератором или администратором.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author or
            request.user.role in ['moderator', 'admin']
        )
