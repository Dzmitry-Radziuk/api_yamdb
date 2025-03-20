from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    pass

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = sum(review.score for review in reviews) / reviews.count()
        else:
            self.rating = None
        self.save()


class Comment(models.Model):
    """
    Модель для хранения комментариев к отзывам.
    """
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.author.username} - {self.review.title.name}'


class Review(models.Model):
    """
    Модель для хранения отзывов на произведения.
    """
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Минимальная оценка'),
            MaxValueValidator(10, 'Максимальная оценка')
        ],
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'{self.author.username} - {self.title.name}'

    # def clean(self):
    #     if self.score < 1 or self.score > 10:
    #         raise ValidationError({'score': 'Оценка должна быть от 1 до 10.'})
    #     if Review.objects.filter(author=self.author, title=self.title).exists():
    #         raise ValidationError({'author': 'Вы уже оставляли отзыв на это произведение.'})

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для обновления рейтинга произведения.
        """
        # self.full_clean()
        super().save(*args, **kwargs)
        self.title.update_rating()

    def delete(self, *args, **kwargs):
        """
        Переопределение метода delete для обновления рейтинга произведения.
        """
        title = self.title
        super().delete(*args, **kwargs)
        title.update_rating()
