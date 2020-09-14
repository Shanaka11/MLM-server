from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.db import transaction
from .serializers import UserSerializer, UserProfileSerializer, PublicUserSerializer
from rest_framework.decorators import api_view
import jwt
import base64
import datetime
from .models import Role, UserProfile
from commissions.serializers import SalespersonSeralizer
from django.core.mail import send_mail

key = 'kahdojnsjh61vhjrfh1g23'
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

# Reset Password
@api_view(('POST', ))
def password_change_req(request):
    # Validate the email and Genorate a token, Send the token to the email given
    user = User.objects.get(username=request.data["username"])
    # Check if a user exists, if so genarate the token and send the e mail
    # Genarate a token
    if user:
        # Basic Token
        # token = random.uniform(10000, 10000000)
        # reset_entry = PasswordResetToken.objects.create(
        #     username = user,
        #     token= token
        # )
        # # if the token exists remove it before saving
        # if reset_entry:
        #     reset_entry.delete()
        # reset_entry.save()
        # JWT Token
        token = jwt.encode({'name': user.username, 'exp': datetime.datetime.now()}, key, algorithm='HS256').decode() 
        # Url to be sent to the e mail
        url = "http://127.0.0.1:8000/api/user/reset_password/" + user.username + "/" + token
        # Send Email
        send_mail(
            'Reset Password',
            'Click the link to reset password ' + url,
            'NoReply@admin.com',
            [user.email],
        )
        return Response({"message": "An Email was sent to " + user.email +" ,Follow the instructions to reset your password"}, status=200)
    else:
        return Response({"message": "User Does not exist"}, status=404)

#@action(methods=['POST'], detail=False, url_path='reset_password/(?P<username>[\w-]+)/(?P<token>[\w\.\'-]+)')
@api_view(('POST', ))
def reset_password(request, username=None, token=None):
    # Check the token an if vaidated save new password
    # Basic Token
    # reset_entry = PasswordResetToken.objects.get(token=token)
    # JWT Token
    test = bytes(token, 'utf-8')
    decode_token = jwt.decode(test, key, algorithms='HS256')
    # if token is valud then do the password change
    if (datetime.datetime.now() - datetime.datetime.utcfromtimestamp(0)).total_seconds() - decode_token["exp"] <= 300:
        # Check passwords
        if(request.data["password"] == request.data["password2"]):
            user = User.objects.get(username=username)
            user.set_password(request.data["password"])
            user.save()
            # Remove the token
            # reset_entry.delete()
            return Response({"message": "Password Changed"}, status=201)
        else:
            return Response({"message": "Passwords Do Not Match"}, status=400)
    else:
        return Response({"message": "Token is invalid"}, status=404)
