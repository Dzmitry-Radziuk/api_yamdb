import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.timezone import now
from rest_framework import serializers
from django.conf import settings

from api_yamdb.settings import (
    FORBIDDEN_NAME,
    MAX_LENGTH_SLUG,
    SLUG_REGEX_PATTERN
)

username_validator = RegexValidator(
    regex=settings.USERNAME_REGEX,
    message=("Введите корректное имя пользователя. "
             "Допустимы буквы, цифры и символы @/./+/-/_.")
)


def doc(docstring):
    """Декоратор для установки docstring."""

    def decorator(func):
        func.__doc__ = docstring
        return func

    return decorator


def username_not_me_validator(value):
    if value == FORBIDDEN_NAME:
        raise ValidationError(
            f"Нельзя использовать \"{FORBIDDEN_NAME}\" в качестве никнейма.")


@doc(
    "Проверяет, что slug состоит только из букв,"
    "цифр, дефиса и подчёркивания."
    f"Максимальная длина: {MAX_LENGTH_SLUG} символов."
)
def validate_slug(value):
    if not re.match(SLUG_REGEX_PATTERN, value):
        raise serializers.ValidationError(
            "Slug должен содержать только буквы, цифры, "
            "дефис или подчёркивание."
        )
    if len(value) > MAX_LENGTH_SLUG:
        raise serializers.ValidationError(
            f"Slug не должен превышать {MAX_LENGTH_SLUG} символов."
        )
    return value


def validate_year(value):
    """Проверяет, что год не превышает текущий."""
    if value > now().year:
        raise serializers.ValidationError(
            "Год выпуска не может быть больше текущего года."
        )
    return value


def validate_unique_slug(data, model, instance=None):
    """Проверяет уникальность slug для заданной модели."""
    slug = data.get('slug')
    if model.objects.exclude(
            id=getattr(instance, "id", None)).filter(slug=slug).exists():
        raise serializers.ValidationError(
            {'slug': f"{model.__name__} с таким slug уже существует."}
        )
    return data


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


def validate_role(role):
    """Проверяет, является ли роль допустимой."""
    if role not in dict(settings.ROLE_CHOICES):
        raise ValidationError("Передана недопустимая роль.")
    return role
