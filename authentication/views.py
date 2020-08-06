from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.decorators import api_view

from .models import Role
from commissions.serializers import SalespersonSeralizer

max_age = 365 * 24 * 60 * 60

class TokenObtainPairViewNew(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop('refresh')
        response.set_cookie('refresh', refresh, max_age=max_age)
        curruser = User.objects.get(username=request.data['username'])
        response.data['user'] = UserSerializer(curruser).data
        return response

class TokenRefreshViewNew(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES['refresh']
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop('refresh')
        response.set_cookie('refresh', refresh, max_age=max_age, httponly=True)
        return response


@api_view(('GET',))
def getUser(request):
    serializer = UserSerializer(request.user)
    return Response(data=serializer.data, status=200)

class CreateUserView(APIView):

    def post(self, request):
        user = request.data
        serializer_user = UserSerializer(data = user)
        # IF CLIENT the fetch client Role object and assign it 
        # Assume its client for now
        serializer_salesperson = SalespersonSeralizer(data = user)
    
        if serializer_user.is_valid() and serializer_salesperson.is_valid():
            serializer_user.save()
            # Then Create the userprofile and the salesperson       
            serializer_salesperson.save()

        else:
            return Response({'response': 'error', 'message': serializer_user.errors})
        return Response({'response': 'success'}, status=201)
    
    # def get(self, request):
    #     users = User.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     # if serializer.is_valid():
    #     return Response(serializer.data, status=200)    
    #     # return Response(serializer.errors, status=400)
