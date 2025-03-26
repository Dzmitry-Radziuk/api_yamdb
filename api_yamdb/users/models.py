from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import Truncator

from api.common import constants
from users.validators import username_validator, validate_forbidden_username


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        max_length=constants.MAX_LENGTH_NAME,
        unique=True,
        validators=[username_validator, validate_forbidden_username],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
        verbose_name='Имя пользователя'
    )

    email = models.EmailField(
        unique=True,
        max_length=constants.MAX_LENGTH_EMAIL,
        verbose_name='Email'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=constants.MAX_LENGTH_ROLE,
        choices=constants.ROLE_CHOICES,
        default=constants.USER,
        verbose_name='Роль'
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return Truncator(self.username).chars(constants.MAX_LENGTH_STR)

    @property
    def is_admin(self):
        return self.role == constants.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == constants.MODERATOR
