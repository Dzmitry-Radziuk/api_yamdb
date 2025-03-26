from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_year(value):
    """Проверяет, что год не превышает текущий."""
    if value > now().year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего года.'
        )
    return value
