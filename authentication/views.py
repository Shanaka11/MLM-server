from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.db import transaction
from .serializers import UserSerializer, UserProfileSerializer, PublicUserSerializer
from rest_framework.decorators import api_view

from .models import Role, UserProfile
from commissions.serializers import SalespersonSeralizer

max_age = 365 * 24 * 60 * 60

class TokenObtainPairViewNew(TokenObtainPairView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop('refresh')
        response.set_cookie('refresh', refresh, max_age=max_age)
        curruser = User.objects.get(username=request.data['username'])
        response.data['user'] = UserSerializer(curruser).data
        return response

class TokenRefreshViewNew(TokenRefreshView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES['refresh']
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop('refresh')
        response.set_cookie('refresh', refresh, max_age=max_age, httponly=True)
        return response


@api_view(('GET',))
def getUser(request):
    serializer = PublicUserSerializer(request.user)
    return Response(data=serializer.data, status=200)

class CreateUserView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.data
        serializer_user = UserSerializer(data = user)

        if serializer_user.is_valid():
            serializer_user.save()
            # IF CLIENT the fetch client Role object and assign it 
            # Assume its client for now
            user['user'] = serializer_user.data['id']
            sponser_user = User.objects.get(username = request.data['sponser'])
            user['sponser'] = sponser_user.salesperson.id
            serializer_salesperson = SalespersonSeralizer(data = user)              
            if serializer_salesperson.is_valid():
                # Then Create the salesperson       
                serializer_salesperson.save()
            else:
                print(serializer_salesperson.errors)
                raise serializers.ValidationError(serializer_salesperson.errors)
        else:
            return Response({'response': 'error', 'message': serializer_user.errors})
        return Response({'response': 'success'}, status=201)
    
    # def get(self, request):
    #     users = User.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     # if serializer.is_valid():
    #     return Response(serializer.data, status=200)    
    #     # return Response(serializer.errors, status=400)

@api_view(('POST',))
@transaction.atomic
def CreateAdmin(request):
        user = User.objects.create(
            username=request.data['username'],
            first_name=request.data['first_name'],
            email=request.data["email"]
        )
        user.set_password(request.data["password"])
        user.save()
        # Create User Profile
        role = Role.objects.get(role ='ADMIN')
        profile = UserProfile.objects.create(
            user = user,
            role = role,
            cell = request.data["cell"]
        )        
        profile.save()  

        return Response({"response": "Admin Created"}, status=201)
        
@api_view(('POST', ))
@transaction.atomic
def UpdateUser(request):
    user = User.objects.get(username= request.data['username'])
    if request.data['type'] == 'email':
        if request.data['email']:
            user.email = request.data['email']

    if request.data['type'] == 'password':
        if request.data['password']:
            user.set_password(request.data['password'])
    user.save()
    return Response({"response": "User Updated"}, status=203)
