from rest_framework.viewsets import ModelViewSet
from users.models import CustomUser
from users.serializers import UserSerializer
from users.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]