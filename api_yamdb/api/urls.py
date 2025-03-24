from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       CommentViewSet, ReviewViewSet, SignupView,
                       TokenViewSet, UserViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
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
    path('', include(router_v1.urls)),
]
