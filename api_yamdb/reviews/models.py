from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from django.utils.text import Truncator

from titles.models import Title
from users.models import User


class BaseTextModel(models.Model):
    """Абстрактная модель для хранения текста, автора и даты публикации."""

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        truncated_author = Truncator(self.author.username).chars(
            settings.MAX_LENGTH_STR
        )
        truncated_text = Truncator(self.text).chars(
            settings.MAX_LENGTH_TEXT
        )
        return f'{truncated_author} - {truncated_text}'


class Comment(BaseTextModel):
    """Модель для хранения комментариев к отзывам."""

    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(BaseTextModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        truncated_author = Truncator(self.author.username).chars(
            settings.MAX_LENGTH_STR
        )
        truncated_review = Truncator(self.review.text).chars(
            settings.MAX_LENGTH_TEXT
        )
        return f'{truncated_author} - {truncated_review}'


class Review(BaseTextModel):
    """Модель для хранения отзывов на произведения."""

    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                settings.MIN_REVIEW_SCORE,
                settings.MIN_REVIEW_SCORE_MSG
            ),
            MaxValueValidator(
                settings.MAX_REVIEW_SCORE,
                settings.MAX_REVIEW_SCORE_MSG
            )
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta(BaseTextModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        truncated_author = Truncator(self.author.username).chars(
            settings.MAX_LENGTH_STR
        )
        truncated_title = Truncator(self.title.name).chars(
            settings.MAX_LENGTH_TEXT
        )
        return f'{truncated_author} - {truncated_title}'
