from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SignupViewSet, TokenViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'auth/signup/',
        SignupViewSet.as_view({'post': 'create'}), name='signup'),
    path(
        'auth/token/',
        TokenViewSet.as_view({'post': 'create'}), name='token'),
    path('', include(router.urls)),
]
