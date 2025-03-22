from django.db import models
from django.utils.timezone import now
from rest_framework import serializers

from titles.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ['name','slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ['name', 'slug']
        


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений (вложенные объекты)."""

    category = CategorySerializer(
        read_only=True
    )
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = [
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        ]

    def get_rating(self, obj):
        """Возвращает средний рейтинг произведения."""
        return obj.reviews.aggregate(average=models.Avg('score'))['average']


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи произведений (slug вместо объектов)."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = [
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        ]

    def validate_year(self, value):
        """Запрещает указывать год выпуска больше текущего."""
        if value > now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего года.')
        return value
