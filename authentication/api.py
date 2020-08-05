from rest_framework import viewsets
from .serializers import RoleSerializer, UserProfileSerializer
from .models import Role, UserProfile


class RoleApi(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserProfileApi(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

