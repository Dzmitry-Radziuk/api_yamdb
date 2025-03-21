from datetime import datetime

from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter
from rest_framework import serializers

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
    year = NumberFilter(
        field_name='year',
        lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


def validate_year(year):
    """Проверяет, что год выпуска не больше текущего."""
    if year and year > datetime.now().year:
        raise serializers.ValidationError(
            "Год выпуска не может быть больше текущего.")
    return year
