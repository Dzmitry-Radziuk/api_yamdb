from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from api.common.constants import FORBIDDEN_USERNAMES, USERNAME_REGEX

username_validator = RegexValidator(
    regex=USERNAME_REGEX,
    message=('Введите корректное имя пользователя. '
             f'Допустимы буквы, цифры и символы {USERNAME_REGEX}')
)


def validate_forbidden_username(username):
    """Проверяет, что username не запрещён."""
    if username in FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Использование \"{username}\" в качестве username запрещено.')
