from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import SignupView, TokenViewSet, UserViewSet
from reviews.views import CommentViewSet, ReviewViewSet
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
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

auth_urls = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenViewSet.as_view({'post': 'create'}), name='token'),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router.urls)),
]
