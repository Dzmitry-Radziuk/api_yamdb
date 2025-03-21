import random
import string

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from users.constants import ROLE_CHOICES


def generate_confirmation_code(length=6):
    """Генерирует случайный 6-значный код подтверждения."""
    return ''.join(random.choices(string.digits, k=length))


def send_confirmation_email(email, confirmation_code):
    """Отправляет email с кодом подтверждения (с логом)."""
    print(f'📧 Sending confirmation email to {email}: {confirmation_code}')
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
    """
    Проверяет наличие обязательных полей в data.
    Возвращает словарь ошибок для отсутствующих полей.
    """
    errors = {}
    for field in fields:
        if not data.get(field):
            errors[field] = ['Это поле обязательно.']
    return errors


def prepare_user_creation_data(data, default_role):
    """
    Подготавливает данные для создания пользователя:
    - Если передана роль, валидирует её;
    иначе подставляет значение по умолчанию.
    - Добавляет зашифрованный пустой пароль.
    - Генерирует confirmation_code, если он не передан.
    """
    data = data.copy()
    role = data.get("role", default_role)
    if "role" in data:
        validate_role(role)
    data['role'] = role
    data['password'] = make_password(None)
    data.setdefault('confirmation_code', generate_confirmation_code())
    return data
