from django.contrib import admin

from titles.models import Category, Genre, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
    ]
    search_fields = [
        'name',
    ]
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
    ]
    search_fields = [
        'name',
    ]
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'year',
        'category',
        'get_genres',
    ]
    list_filter = [
        'year',
        'category',
    ]
    search_fields = [
        'name',
    ]
    filter_horizontal = [
        'genre',
    ]
    list_editable = [
        'category',
    ]

    @admin.display(description='Жанры')
    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
