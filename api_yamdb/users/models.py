from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (ADMIN, MAX_LENGTH_STR, MODERATOR, ROLE_CHOICES,
                             USER)
from users.validators import username_validator


class User(AbstractUser):
    """Кастомная модель пользователя."""
    
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
        verbose_name='Имя пользователя'
    )

    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Email'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:MAX_LENGTH_STR] + (
            "..." if len(self.username) > MAX_LENGTH_STR else ""
        )

    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    def is_moderator(self):
        return self.role == MODERATOR

    def is_user(self):
        return self.role == USER
