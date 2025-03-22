from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.paginations import UserPagination
from api.permissions import IsAdmin, IsUserOrAdminOrModerator
from api.serializers import SignupSerializer, TokenSerializer, UserSerializer
from api.utils import send_confirmation_email
from users.models import User


class SignupView(APIView):
    """Регистрация пользователя."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_confirmation_email(user.email, user.confirmation_code)
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

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsUserOrAdminOrModerator, IsAuthenticated])
    def me(self, request):
        """Возвращает или обновляет профиль текущего пользователя."""
        if request.method == 'PATCH':
            data = request.data.copy()
            data.pop('role', None)
            serializer = self.get_serializer(
                request.user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(self.get_serializer(request.user).data)
