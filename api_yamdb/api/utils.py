from datetime import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from titles.models import Title
from users.constants import ROLE_CHOICES, USER


def generate_confirmation_code(user):
    """Генерирует токен подтверждения для пользователя."""
    return default_token_generator.make_token(user)


def send_confirmation_email(email, confirmation_code):
    """Отправляет email с кодом подтверждения (с логом)."""
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


def validate_role(role):
    """Проверяет, является ли роль допустимой."""
    if role not in dict(ROLE_CHOICES):
        raise ValidationError("Передана недопустимая роль.")
    return role


def check_required_fields(data, fields):
    """Проверяет наличие обязательных полей в data."""
    errors = {}
    for field in fields:
        if not data.get(field):
            errors[field] = ['Это поле обязательно.']
    return errors


def prepare_user_creation_data(data, default_role=USER):
    """Подготавливает данные для создания пользователя."""
    data = data.copy()
    role = data.get("role", default_role)
    if "role" in data:
        validate_role(role)
    data['role'] = role
    data['password'] = make_password(None)
    data.pop('confirmation_code', None)
    return data


class TitleFilter(FilterSet):
    """Фильтрация произведений по slug категории и жанра, названию и году."""

    category = CharFilter(
        field_name='category__slug',
        lookup_expr='exact'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='exact'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = NumberFilter(
        field_name='year',
        lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


def validate_year(year):
    """Проверяет, что год выпуска не больше текущего."""
    if year and year > datetime.now().year:
        raise serializers.ValidationError(
            "Год выпуска не может быть больше текущего.")
    return year