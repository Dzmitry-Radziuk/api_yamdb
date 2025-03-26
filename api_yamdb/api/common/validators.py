from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Review
from users.models import User


def validate_unique_username_email(data):
    """Проверяет уникальность username и email."""
    username = data.get('username')
    email = data.get('email')

    user_qs = User.objects.filter(username=username)
    if user_qs.exists():
        user = user_qs.first()
        if user.email != email:
            raise ValidationError(
                "Пользователь с таким username уже существует.")

    email_qs = User.objects.filter(email=email)
    if email_qs.exists():
        user = email_qs.first()
        if user.username != username:
            raise ValidationError(
                "Пользователь с таким email уже существует.")


def validate_role(serializer, role):
    """Запрещает изменять роль обычным пользователям."""
    user = serializer.context['request'].user

    if not user.is_admin:
        raise serializers.ValidationError("Изменение роли запрещено.")
    return role


def get_score_validators():
    """Возвращает список валидаторов для оценки из модели Review."""
    return Review._meta.get_field('score').validators


def validate_unique_review(data, context):
    """Пользователь оставляет не более одного отзыва на произведение."""
    request = context.get('request')

    if request and request.method == 'POST':
        title_id = context.get('view').kwargs.get('title_id')
        if Review.objects.filter(
                author=request.user, title_id=title_id).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на это произведение."
            )
    return data
