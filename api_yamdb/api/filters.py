from django_filters.rest_framework import (
    CharFilter, FilterSet)

from titles.models import Title


class TitleFilter(FilterSet):
    """Фильтрация произведений по slug категории и жанра, названию и году."""

    category = CharFilter(
        field_name='category__slug',
        lookup_expr='exact'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='exact'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
