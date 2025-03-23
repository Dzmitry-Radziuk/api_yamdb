from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models

from titles.constants import MAX_LENGTH_NAME, MAX_STR_LENGTH


class NameSlugModel(models.Model):
    """Абстрактная модель для объектов с именем и slug."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name[:MAX_STR_LENGTH]


class Category(NameSlugModel):
    """Модель категории произведений."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    """Модель жанра произведений."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[MaxValueValidator(datetime.now().year)],
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name[:MAX_STR_LENGTH]
