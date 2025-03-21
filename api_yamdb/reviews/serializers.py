from rest_framework import serializers

from reviews.models import Comment, Review
from reviews.utils import summarize_text
from reviews.validators import (validate_score, validate_text,
                                validate_unique_review)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    text = serializers.CharField(
        required=True,
        allow_blank=False,
        validators=[validate_text]
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ['id', 'pub_date']

    def get_text(self, obj):
        return summarize_text(obj.text)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    text = serializers.CharField(
        required=True,
        allow_blank=False,
        validators=[validate_text]
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=validate_score()
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'score', 'author', 'pub_date']

    def validate(self, data):
        return validate_unique_review(data, self.context)
