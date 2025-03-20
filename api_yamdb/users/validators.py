from django.core.validators import RegexValidator

username_validator = RegexValidator(
    regex=r'^[\w.@+-]+\Z',
    message=('Введите корректное имя пользователя. '
             'Допустимы буквы, цифры и символы @/./+/-/_.')
)
