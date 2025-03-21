from rest_framework.generics import get_object_or_404

from reviews.models import Review, Title


def get_title_by_id(kwargs):
    """Получает объект произведения по `title_id`."""
    return get_object_or_404(Title, id=kwargs.get('title_id'))


def get_review_by_id(kwargs):
    """Получает объект отзыва по `review_id`."""
    return get_object_or_404(Review, id=kwargs.get('review_id'))


def summarize_text(text, word_limit=3):
    """Обрезает текст, добавляя `...`, если текст длиннее."""
    words = text.split()
    return (' '.join(words[:word_limit]) + '...'
            if len(words) > word_limit else text)
