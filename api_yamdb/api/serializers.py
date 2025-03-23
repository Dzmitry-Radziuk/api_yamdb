from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.exceptions import InvalidConfirmationCode, UserNotFound
from api.utils import generate_confirmation_code
from api.validators import (username_not_me_validator, username_validator,
                            validate_slug, validate_unique_slug, validate_year)
from titles.models import Category, Genre, Title
from users.constants import (FORBIDDEN_USERNAMES, MAX_LENGTH_EMAIL,
                             MAX_LENGTH_NAME)
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
    """Сериализатор регистрации пользователя."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_LENGTH_NAME,
        validators=[username_validator, username_not_me_validator]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_LENGTH_EMAIL,
        validators=[]
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, data):
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

        if username.lower() in FORBIDDEN_USERNAMES:
            raise ValidationError(
                f"Использование \"{username}\" в качестве username запрещено."
            )
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(None)
        user, _ = User.objects.get_or_create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            defaults=validated_data
        )
        new_code = generate_confirmation_code(user)
        user.confirmation_code = new_code
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise UserNotFound()
        if user.confirmation_code != confirmation_code:
            raise InvalidConfirmationCode()
        data['user'] = user
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    slug = serializers.CharField(validators=[validate_slug])

    def validate(self, data):
        """Проверяет уникальность slug через валидатор."""
        return validate_unique_slug(data, Category, self.instance)

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    slug = serializers.CharField(validators=[validate_slug])

    def validate(self, data):
        """Проверяет уникальность slug через валидатор."""
        return validate_unique_slug(data, Genre, self.instance)

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений (вложенные объекты)."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre', 'category']


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи произведений (slug вместо объектов)."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_empty=False
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'description', 'genre', 'category']
