from django.contrib import admin

from reviews.models import Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'title',
        'score',
        'pub_date',
    ]
    list_filter = [
        'score',
        'pub_date',
    ]
    search_fields = [
        'author__username',
        'title__name',
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'review',
        'pub_date',
    ]
    list_filter = [
        'pub_date',
    ]
    search_fields = [
        'author__username',
        'review__text',
    ]
