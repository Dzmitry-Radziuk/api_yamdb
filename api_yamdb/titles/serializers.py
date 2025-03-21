import datetime
from rest_framework import serializers
from django.db import models
from titles.models import Category, Genre, Title
from reviews.models import Review  # Импортируем модель отзывов

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')

class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def get_rating(self, obj):
        """Вычисляет средний рейтинг из отзывов."""
        reviews = Review.objects.filter(title=obj)
        return reviews.aggregate(average_rating=models.Avg('score'))['average_rating']

class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        """Запрещает указывать год выпуска больше текущего."""
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Год выпуска не может быть больше текущего года.')
        return value

    def validate_category(self, value):
        """Проверяет существование категории."""
        if not Category.objects.filter(slug=value.slug).exists():
            raise serializers.ValidationError('Выбранная категория не существует.')
        return value