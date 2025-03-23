from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import CommentViewSet, ReviewViewSet
from api.views import TitleViewSet

router = DefaultRouter()
router.register('title', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
