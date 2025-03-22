from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import SignupView, TokenViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenViewSet.as_view({'post': 'create'}), name='token'),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router.urls)),
]
