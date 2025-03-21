from rest_framework.pagination import PageNumberPagination

from users.constants import MAX_PAGE_SIZE, PAGE_SIZE


class UserPagination(PageNumberPagination):
    """Кастомная пагинация для пользователей"""

    page_size = PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = MAX_PAGE_SIZE
