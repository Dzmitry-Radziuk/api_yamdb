from django.contrib import admin

from titles.models import Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админ-панель для управления произведениями."""

    list_display = ['id', 'name', 'year', 'category', 'rating']
    list_filter = ['year', 'category', 'genre']
    search_fields = ['name',]
    autocomplete_fields = ['category', 'genre']
    readonly_fields = ['rating',]
