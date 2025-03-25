from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.timezone import now
from rest_framework import serializers

from api.common.constants import (FORBIDDEN_USERNAMES, MAX_LENGTH_SLUG,
                                  USERNAME_REGEX)

username_validator = RegexValidator(
    regex=USERNAME_REGEX,
    message=(f"Введите корректное имя пользователя. "
             f"Допустимы буквы, цифры и символы {USERNAME_REGEX}")
)


def validate_unique_username_email(data):
    """Проверяет уникальность username и email."""
    from users.models import User
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


def validate_forbidden_username(username):
    """Проверяет, что username не запрещён."""
    if username in FORBIDDEN_USERNAMES:
        raise ValidationError(
            f"Использование \"{username}\" в качестве username запрещено.")


def doc(docstring):
    """Декоратор для установки docstring."""

    def decorator(func):
        func.__doc__ = docstring
        return func

    return decorator


@doc(
    "Проверяет, что slug состоит только из букв,"
    "цифр, дефиса и подчёркивания."
    f"Максимальная длина: {MAX_LENGTH_SLUG} символов."
)
def validate_year(value):
    """Проверяет, что год не превышает текущий."""
    if value > now().year:
        raise serializers.ValidationError(
            "Год выпуска не может быть больше текущего года."
        )
    return value


def get_score_validators():
    """Возвращает список валидаторов для оценки из модели Review."""
    from reviews.models import Review
    return Review._meta.get_field('score').validators


def validate_unique_review(data, context):
    """Пользователь оставляет не более одного отзыва на произведение."""
    from reviews.models import Review
    request = context.get('request')

    if request and request.method == 'POST':
        title_id = context.get('view').kwargs.get('title_id')
        if Review.objects.filter(
                author=request.user, title_id=title_id).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на это произведение."
            )
    return data


def validate_role(serializer, role):
    """Запрещает изменять роль обычным пользователям."""
    user = serializer.context['request'].user

    if not user.is_admin:
        raise serializers.ValidationError("Изменение роли запрещено.")

    return role
