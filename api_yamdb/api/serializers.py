from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.text import Truncator
from rest_framework import serializers

from api.common.constants import (MAX_LENGTH_EMAIL, MAX_LENGTH_NAME,
                                  MAX_LENGTH_TEXT, ROLE_CHOICES)
from api.common.utils import (generate_confirmation_code,
                              send_confirmation_email)
from api.common.validators import (username_validator,
                                   validate_forbidden_username,
                                   validate_year)
from api.common.model_validators import (
    get_score_validators, validate_role,
    validate_unique_review, validate_unique_username_email
)
from api.exceptions import InvalidConfirmationCode, UserNotFound
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        required=False,
    )

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

    def validate_role(self, role):
        return validate_role(self, role)


class SignupSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_LENGTH_NAME,
        validators=[username_validator, validate_forbidden_username]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_LENGTH_EMAIL,
    )

    def validate(self, data):
        validate_unique_username_email(data)
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(None)
        user, _ = User.objects.get_or_create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            defaults=validated_data
        )
        send_confirmation_email(user.email, generate_confirmation_code(user))
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

        if not default_token_generator.check_token(user, confirmation_code):
            raise InvalidConfirmationCode()

        data['user'] = user
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений (вложенные объекты)."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = [
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        ]


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

    def to_representation(self, instance):
        """Возвращает данные в формате TitleReadSerializer."""
        return TitleReadSerializer(instance).data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']

    def get_text(self, obj):
        return Truncator(obj.text).chars(MAX_LENGTH_TEXT)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=get_score_validators()
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'score', 'author', 'pub_date']

    def validate(self, data):
        return validate_unique_review(data, self.context)
