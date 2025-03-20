from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, data):
        """
        Валидирует данные для регистрации:
        проверяет совпадение username и email, запрещает 'me'.
        """
        username = data.get('username')
        email = data.get('email')
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            user = user_qs.first()
            if user.email != email:
                raise ValidationError(
                    "Пользователь с таким username уже существует.")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            user = email_qs.first()
            if user.username != username:
                raise ValidationError(
                    "Пользователь с таким email уже существует.")
        if username.lower() == "me":
            raise ValidationError(
                'Использование "me" в качестве username запрещено.')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
