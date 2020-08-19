from rest_framework import viewsets
from .serializers import RoleSerializer, UserProfileSerializer, ReadUserProfileSerializer, DocumentSerializer, AdsSerializer
from .models import Role, UserProfile, Document, Ads
from django.contrib.auth import authenticate
from rest_framework.response import Response

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
    
class AdsApi(viewsets.ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer

    def create(self, request):
        # Validate user and then proceed
        user = authenticate(request, username= request.data['username'], password= request.data['password'])
        if user is not None:
            return super().create(request)
        else:
            return Response({"message": "Invalid Credentials"}, status = 400)
