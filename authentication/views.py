from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view

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
        serializer = UserSerializer(data = user)
        if serializer.is_valid():
            saved_user = serializer.save()
            # Then Create the userprofile and the salesperson
        else:
            return Response({'response': 'error', 'message': serializer.errors})
        return Response({'response': 'success'}, status=201)
