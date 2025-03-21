from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from titles.models import Category, Genre, Title
from titles.permissions import AdminOrReadOnly
from titles.serializers import (CategorySerializer, GenreSerializer,
                                TitleReadSerializer, TitleWriteSerializer)

from .exceptions import MethodNotAllowedException
from .utils import TitleFilter, validate_year


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD для категорий. Доступен только администратору."""

    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']
    http_method_names = [
        'get',
        'post',
        'delete'
    ]

    def get_queryset(self):
        return Category.objects.order_by('name')

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowedException("GET")


class GenreViewSet(viewsets.ModelViewSet):
    """CRUD для жанров. Доступен только администратору."""

    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']
    http_method_names = [
        'get',
        'post',
        'delete'
    ]

    def get_queryset(self):
        return Genre.objects.order_by('name')

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowedException("GET")


class TitleViewSet(viewsets.ModelViewSet):
    """CRUD для произведений. Чтение доступно всем, управление — админам."""

    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete'
    ]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_permissions(self):
        """Чтение доступно всем, управление — только администраторам."""
        if self.action in ('list', 'retrieve'):
            return []
        return [AdminOrReadOnly()]

    def perform_create(self, serializer):
        """Валидация: нельзя добавлять произведения из будущего."""
        year = serializer.validated_data.get('year')
        serializer.validated_data['year'] = validate_year(year)
        serializer.save()
