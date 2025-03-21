from django.contrib import admin

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка для пользователей."""

    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
    search_fields = ['username', 'email']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий."""

    list_display = ('id', 'name', 'slug')
    search_fields = ['name', 'slug']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для жанров."""

    list_display = ('id', 'name', 'slug')
    search_fields = ['name', 'slug']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка для произведений."""

    list_display = ('id', 'name', 'year', 'category', 'rating')
    list_filter = ('year', 'category', 'genre')
    search_fields = ['name']
    autocomplete_fields = ('category', 'genre')
    readonly_fields = ('rating',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для отзывов."""

    list_display = ('id', 'text', 'author', 'score', 'pub_date', 'title')
    list_filter = ('score', 'author', 'title')
    search_fields = ['text', 'author__username']
    autocomplete_fields = ('author', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев."""

    list_display = ('id', 'text', 'author', 'review', 'pub_date')
    search_fields = ['text', 'author__username', 'review__title__name']
    autocomplete_fields = ('author', 'review')
