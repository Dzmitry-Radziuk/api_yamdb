from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ("Персональная информация",
         {'fields': ('first_name', 'last_name', 'bio')}),
        ('Права доступа', {'fields': ('role', 'is_staff', 'is_superuser')}),
    )
