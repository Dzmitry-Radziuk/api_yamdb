from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import Truncator

from api.validators import username_not_me_validator, username_validator
from users.constants import (ADMIN, MAX_LENGTH_CONFIRM_CODE, MAX_LENGTH_EMAIL,
                             MAX_LENGTH_NAME, MAX_LENGTH_ROLE, MAX_LENGTH_STR,
                             MODERATOR, ROLE_CHOICES, USER)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        max_length=MAX_LENGTH_NAME,
        unique=True,
        validators=[username_validator, username_not_me_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
        verbose_name='Имя пользователя'
    )

    email = models.EmailField(
        unique=True,
        max_length=MAX_LENGTH_EMAIL,
        verbose_name='Email'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=MAX_LENGTH_CONFIRM_CODE,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return Truncator(self.username).chars(MAX_LENGTH_STR)

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser
    
    @property
    def is_moderator(self):
        return self.role == MODERATOR
