from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (SAFE_METHODS, AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.common.utils import get_review_by_id, get_title_by_id
from api.filters import TitleFilter
from api.paginations import UserPagination
from api.permissions import (AdminOrReadOnly, IsAdmin,
                             IsAuthorOrModeratorOrAdmin)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer, TitleReadSerializer,
                             TitleWriteSerializer, TokenSerializer,
                             UserSerializer)
from titles.models import Category, Genre, Title
from users.models import User


class SignupView(APIView):
    """Регистрация пользователя."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {'username': user.username, 'email': user.email},
            status=status.HTTP_200_OK
        )


class TokenViewSet(viewsets.ViewSet):
    """Получение JWT-токена."""

    permission_classes = [AllowAny]

    def create(self, request):
        """Обрабатывает запрос на получение токена после валидации."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователями (CRUD-операции)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = UserPagination
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated & IsAuthorOrModeratorOrAdmin]
    )
    def me(self, request):
        """Возвращает или обновляет профиль текущего пользователя."""

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


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
    ).order_by('name')

    permission_classes = [AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdmin
    ]
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
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdmin
    ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return get_title_by_id(self.kwargs).reviews.select_related(
            'author', 'title')

    def perform_create(self, serializer):
        title = get_title_by_id(self.kwargs)
        serializer.save(author=self.request.user, title=title)
