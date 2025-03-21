from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from reviews.constants import MAX_REVIEW_SCORE, MIN_REVIEW_SCORE
from reviews.models import Review


def validate_score():
    """Возвращает валидатор для оценки (от 1 до 10)."""
    return [
        MinValueValidator(MIN_REVIEW_SCORE),
        MaxValueValidator(MAX_REVIEW_SCORE)
    ]


def validate_text(value):
    """Запрещает пустые отзывы и комментарии."""
    if not value.strip():
        raise serializers.ValidationError("Текст не может быть пустым.")
    return value


def validate_unique_review(data, context):
    """Пользователь оставляет не более одного отзыва на произведение."""
    request = context.get('request')

    if request and request.method == 'POST':
        title_id = context.get('view').kwargs.get('title_id')
        if Review.objects.filter(
                author=request.user, title_id=title_id
        ).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на это произведение.")
    return data
