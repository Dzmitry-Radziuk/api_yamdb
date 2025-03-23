from django.contrib import admin
from users.models import User
from reviews.models import Comment, Review
from titles.models import Title, Category, Genre


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_superuser')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')
    list_filter = ('year', 'category')
    search_fields = ('name',)
    filter_horizontal = ('genre',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'score', 'pub_date')
    list_filter = ('score', 'pub_date')
    search_fields = ('author__username', 'title__name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'review', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('author__username', 'review__text')
