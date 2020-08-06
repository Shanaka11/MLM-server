from rest_framework import viewsets
from .serializers import RoleSerializer, UserProfileSerializer, ReadUserProfileSerializer
from .models import Role, UserProfile


class RoleApi(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserProfileApi(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_serializer_class(self):
        # Use the create serializer class when adding/updating/removing new objects
        # else use the reguler one
        if self.action == 'list' or self.action == 'retrieve':
            return ReadUserProfileSerializer
        return super().get_serializer_class()
