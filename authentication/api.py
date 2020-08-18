from rest_framework import viewsets
from .serializers import RoleSerializer, UserProfileSerializer, ReadUserProfileSerializer, DocumentSerializer
from .models import Role, UserProfile, Document


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

class DocumentApi(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request):
        agreement = Document.objects.all().first()        
        if agreement is not None:
            agreement.delete()            
        
        return super().create(request)
    
