from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'id',
        'username',
        'email',
        'role',
        'is_staff',
        'is_superuser',
    ]

    search_fields = [
        'username',
        'email',
    ]

    list_filter = [
        'role',
        'is_staff',
        'is_superuser',
    ]

    fieldsets = [
        (
            None,
            {
                'fields': ('username', 'email', 'password')
            }
        ),
        (
            'Персональные данные',
            {
                'fields': (
                    'first_name',
                    'last_name',
                )
            }
        ),
        (
            'Права доступа',
            {
                'fields': (
                    'role',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (
            'Даты',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    ]

    add_fieldsets = [
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'role',
                )
            }
        ),
    ]
