
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from api.common.constants import USER
from api.common.validators import validate_role
from reviews.models import Review, Title
from titles.models import Title


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


def check_required_fields(data, fields):
    """Проверяет наличие обязательных полей в data."""
    errors = {}
    for field in fields:
        if not data.get(field):
            errors[field] = ["Это поле обязательно."]
    return errors


def prepare_user_creation_data(data, default_role=USER):
    """Подготавливает данные для создания пользователя."""
    data = data.copy()
    role = data.get('role', default_role)
    if 'role' in data:
        validate_role(role)
    data['role'] = role
    data['password'] = make_password(None)
    data.pop('confirmation_code', None)
    return data


def get_title_by_id(kwargs):
    """Получает объект произведения по `title_id`."""
    return get_object_or_404(Title, id=kwargs.get('title_id'))


def get_review_by_id(kwargs):
    """Получает объект отзыва по `review_id` и `title_id`."""
    return get_object_or_404(
        Review,
        id=kwargs.get('review_id'),
        title_id=kwargs.get('title_id')
    )
