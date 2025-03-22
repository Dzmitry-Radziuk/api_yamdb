from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

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
