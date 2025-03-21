from django.db import models
from django.db.models import Avg

from titles.constants import (
    MAX_LENGTH_NAME,
    MAX_LENGTH_SLUG,
    MAX_STR_LENGTH
)


class Category(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Идентификатор категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    

    def __str__(self):
        return self.name[:MAX_STR_LENGTH]    


class Genre(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Идентификатор жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:MAX_STR_LENGTH]


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
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
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    rating = models.FloatField(
        null=True, blank=True,
        verbose_name='Рейтинг' 
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def update_rating(self):
        """Обновляет средний рейтинг произведения."""
        avg_rating = self.reviews.aggregate(Avg('score'))['score__avg']
        self.rating = avg_rating if avg_rating is not None else 0
        self.save(update_fields=['rating'])

    def __str__(self):
        return self.name[:MAX_STR_LENGTH]
    
    
