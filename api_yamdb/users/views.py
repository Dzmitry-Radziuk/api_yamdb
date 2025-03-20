from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.constants import USER
from users.exceptions import InvalidConfirmationCode, UserNotFound
from users.models import User
from users.paginations import UserPagination
from users.permissions import IsAdmin, IsUserOrAdminOrModerator
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer
from users.utils import (check_required_fields, generate_confirmation_code,
                         prepare_user_creation_data, send_confirmation_email,
                         validate_role)


class SignupViewSet(viewsets.ViewSet):
    """Регистрация пользователя."""
    permission_classes = [AllowAny]

    def create(self, request):
        """
        Обрабатывает регистрацию: если пользователь существует,
        обновляет confirmation_code,
        иначе — создает нового пользователя с подготовленными данными.
        """
        errors = check_required_fields(request.data, ['username', 'email'])
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        data = prepare_user_creation_data(request.data, USER)
        username = data.get('username')
        email = data.get('email')
        user = User.objects.filter(username=username, email=email).first()
        new_code = generate_confirmation_code()

        if user:
            user.confirmation_code = new_code
            user.save()
        else:
            serializer = SignupSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save(confirmation_code=new_code)

        send_confirmation_email(user.email, new_code)
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
        user = User.objects.filter(
            username=serializer.validated_data['username']).first()
        if not user:
            raise UserNotFound()
        confirmation_code = serializer.validated_data['confirmation_code']
        if user.confirmation_code != confirmation_code:
            raise InvalidConfirmationCode()
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """Управления пользователями (CRUD-операции)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = UserPagination
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email']

    def create(self, request, *args, **kwargs):
        """Создает нового пользователя с подготовленными данными."""
        data = prepare_user_creation_data(request.data, USER)
        serializer = self.get_serializer(
            data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        serializer.instance.role = data['role']
        serializer.instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """Частично обновляет данные пользователя."""
        user = self.get_object()
        data = request.data.copy()
        if 'role' in data:
            validate_role(data['role'])
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsUserOrAdminOrModerator])
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
