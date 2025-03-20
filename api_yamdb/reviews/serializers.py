from rest_framework import serializers 
from reviews.models import Review

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    """
    text = serializers.CharField(required=True, allow_blank=False)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date')

    def get_text(self, obj):
        words = obj.text.split()[:3]
        return ' '.join(words) + '...' if len(obj.text.split()) > 3 else obj.text


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.
    """
    text = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')

    def get_text(self, obj):
        words = obj.text.split()[:3]
        return ' '.join(words) + '...' if len(obj.text.split()) > 3 else obj.text

    def validate(self, data):
        """
        Валидация для проверки, что пользователь
        оставляет только один отзыв на произведение.
        """
        request = self.context.get('request')
        if request.method == 'POST':  # Проверяем только при создании отзыва
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=request.user, title_id=title_id).exists():
                raise serializers.ValidationError('Вы уже оставляли отзыв на это произведение.')
        return data

    def validate_score(self, value):
        """
        Валидация для оценки (должна быть от 1 до 10).
        """
        if value < 1 or value > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10.')
        return value
