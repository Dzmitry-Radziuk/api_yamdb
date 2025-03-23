from rest_framework.pagination import PageNumberPagination

from django.conf import settings


class UserPagination(PageNumberPagination):
    """Кастомная пагинация для пользователей."""

    page_size = settings.PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = settings.MAX_PAGE_SIZE
