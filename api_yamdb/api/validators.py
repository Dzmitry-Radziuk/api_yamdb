import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.timezone import now
from rest_framework import serializers

from titles.constants import MAX_LENGTH_SLUG
from users.constants import USERNAME_REGEX

username_validator = RegexValidator(
    regex=USERNAME_REGEX,
    message=("Введите корректное имя пользователя. "
             "Допустимы буквы, цифры и символы @/./+/-/_.")
)


def username_not_me_validator(value):
    if value.lower() == 'me':
        raise ValidationError(
            "Нельзя использовать \"me\" в качестве никнейма.")

def validate_slug(value):
    """Проверяет, что slug соответствует паттерну ^[-a-zA-Z0-9_]+$ и длине <= 50."""
    if not re.match(r'^[-a-zA-Z0-9_]+$', value):
        raise serializers.ValidationError(
            'Slug должен содержать только буквы, цифры, дефис или подчёркивание.'
        )
    if len(value) > MAX_LENGTH_SLUG:  # MAX_LENGTH_SLUG = 50
        raise serializers.ValidationError(
            f'Slug не должен превышать {MAX_LENGTH_SLUG} символов.'
        )
    return value


def validate_year(value):
    """Проверяет, что год не превышает текущий."""
    if value > now().year:
        raise serializers.ValidationError(
            'Год выпуска не может быть больше текущего года.'
        )
    return value


def validate_unique_slug(data, model, instance=None):
    """Проверяет уникальность slug для заданной модели."""
    slug = data.get('slug')
    if instance is None and model.objects.filter(slug=slug).exists():
        raise serializers.ValidationError(
            {'slug': f'{model.__name__} с таким slug уже существует.'}
        )
    return data