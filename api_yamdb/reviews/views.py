from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from reviews.models import Review, Title
from reviews.permissions import IsAuthorOrModeratorOrAdmin
from reviews.serializers import ReviewSerializer, CommentSerializer


class TitleViewSet(ModelViewSet):
    pass

class CommentViewSet(ModelViewSet):
    """
    Вьюсет для работы с комментариями.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin)

    def get_queryset(self):
        """
        Возвращает комментарии для конкретного отзыва.
        """
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """
        Создает комментарий для конкретного отзыва.
        """
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CommentViewSet(ModelViewSet):
    """
    Вьюсет для работы с комментариями.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin)

    def get_queryset(self):
        """
        Возвращает комментарии для конкретного отзыва.
        """
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """
        Создает комментарий для конкретного отзыва.
        """
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(ModelViewSet):
    """
    Вьюсет для работы с отзывами.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin]

    def get_queryset(self):
        """
        Возвращает отзывы для конкретного произведения.
        """
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """
        Создает отзыв для конкретного произведения.
        """
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        title.update_rating()  # Обновляем рейтинг произведения

    def perform_update(self, serializer):
        """
        Обновляет отзыв и рейтинг произведения.
        """
        super().perform_update(serializer)
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        title.update_rating()  # Обновляем рейтинг произведения

    def perform_destroy(self, instance):
        """
        Удаляет отзыв и обновляет рейтинг произведения.
        """
        title = instance.title
        super().perform_destroy(instance)
        title.update_rating()  # Обновляем рейтинг произведения
