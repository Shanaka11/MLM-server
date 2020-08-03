from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from .serializers import UserSerializer

max_age = 365 * 24 * 60 * 60

class TokenObtainPairViewNew(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop('refresh')
        response.set_cookie('refresh', refresh, max_age=max_age)
        curruser = User.objects.get(username=request.data['username'])
        response.data['user'] = UserSerializer(curruser).data
        return response