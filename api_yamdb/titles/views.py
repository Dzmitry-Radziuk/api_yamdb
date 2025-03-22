from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import SAFE_METHODS

from titles.models import Category, Genre, Title
from titles.permissions import AdminOrReadOnly
from titles.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)
from titles.utils import TitleFilter


class BaseNameSlugViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Базовый вьюсет для категорий и жанров."""
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return self.model.objects.order_by('name')


class CategoryViewSet(BaseNameSlugViewSet):
    """CRUD для категорий. Доступен только администратору."""
    serializer_class = CategorySerializer
    model = Category


class GenreViewSet(BaseNameSlugViewSet):
    """CRUD для жанров. Доступен только администратору."""
    serializer_class = GenreSerializer
    model = Genre

    def perform_create(self, serializer):
        serializer.save()


class TitleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для произведений."""
    queryset = Title.objects.select_related(
        'category'
        ).prefetch_related(
            'genre'
            ).annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    permission_classes = [AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return self.http_method_not_allowed(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)
