
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from reviews.models import Review
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
