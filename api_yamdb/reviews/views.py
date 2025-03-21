from rest_framework.viewsets import ModelViewSet

from reviews.permissions import IsAuthorOrModeratorOrAdmin
from reviews.serializers import CommentSerializer, ReviewSerializer
from reviews.utils import get_review_by_id, get_title_by_id


class CommentViewSet(ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return get_review_by_id(self.kwargs).comments.select_related(
            'author', 'review')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=get_review_by_id(self.kwargs))


class ReviewViewSet(ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return get_title_by_id(self.kwargs).reviews.select_related(
            'author', 'title')

    def perform_create(self, serializer):
        title = get_title_by_id(self.kwargs)
        serializer.save(author=self.request.user, title=title)
        title.update_rating()

    def perform_update(self, serializer):
        instance = self.get_object()
        old_score = instance.score
        super().perform_update(serializer)
        if instance.score != old_score:
            instance.title.update_rating()

    def perform_destroy(self, instance):
        title = instance.title
        super().perform_destroy(instance)
        title.update_rating()
