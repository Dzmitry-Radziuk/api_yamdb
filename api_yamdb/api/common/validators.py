from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.timezone import now
from rest_framework import serializers

from api.common.constants import (FORBIDDEN_USERNAMES, MAX_LENGTH_SLUG,
                                  USERNAME_REGEX)
from api.decorators import doc

username_validator = RegexValidator(
    regex=USERNAME_REGEX,
    message=("Введите корректное имя пользователя. "
             f"Допустимы буквы, цифры и символы {USERNAME_REGEX}")
)


def validate_forbidden_username(username):
    """Проверяет, что username не запрещён."""
    if username in FORBIDDEN_USERNAMES:
        raise ValidationError(
            f"Использование \"{username}\" в качестве username запрещено.")


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
