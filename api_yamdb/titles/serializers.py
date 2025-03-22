from rest_framework import serializers
from titles.models import Category, Genre, Title
from titles.validators import (
    validate_slug,
    validate_year,
    validate_unique_slug
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    slug = serializers.CharField(validators=[validate_slug])

    def validate(self, data):
        """Проверяет уникальность slug через валидатор."""
        return validate_unique_slug(data, Category, self.instance)

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    slug = serializers.CharField(validators=[validate_slug])

    def validate(self, data):
        """Проверяет уникальность slug через валидатор."""
        return validate_unique_slug(data, Genre, self.instance)

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений (вложенные объекты)."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre', 'category']


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи произведений (slug вместо объектов)."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_empty=False
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'description', 'genre', 'category']
