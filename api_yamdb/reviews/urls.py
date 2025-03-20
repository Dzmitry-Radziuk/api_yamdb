from django.urls import include, path
from rest_framework.routers import DefaultRouter
from reviews.views import ReviewViewSet, TitleViewSet, CommentViewSet

router = DefaultRouter()
router.register('title', TitleViewSet)
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