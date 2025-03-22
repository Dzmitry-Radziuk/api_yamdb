import re
from django.utils.timezone import now
from rest_framework import serializers
from titles.constants import MAX_LENGTH_SLUG


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
