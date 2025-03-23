from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import Truncator

from api.common.validators import username_not_me_validator, username_validator
from django.conf import settings


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        unique=True,
        validators=[username_validator, username_not_me_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
        verbose_name='Имя пользователя'
    )

    email = models.EmailField(
        unique=True,
        max_length=settings.MAX_LENGTH_EMAIL,
        verbose_name='Email'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=settings.MAX_LENGTH_ROLE,
        choices=settings.ROLE_CHOICES,
        default=settings.USER,
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=settings.MAX_LENGTH_CONFIRM_CODE,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return Truncator(self.username).chars(settings.MAX_LENGTH_STR)

    @property
    def is_admin(self):
        return self.role == settings.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR
