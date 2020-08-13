from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import User
from .models import Role, UserProfile
# from commissions.serializers import SalespersonSeralizer, Salesperson
from rest_framework.response import Response

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class ReadUserProfileSerializer(serializers.ModelSerializer):

    role = RoleSerializer(UserProfile.role, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # Fetch Role from user profile as well
    # user_profile = UserProfileSerializer()
    # salesperson = SalespersonSeralizer()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'email')

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        # Create User Profile
        role = Role.objects.get(role ='CLIENT')
        profile = UserProfile.objects.create(
            user = user,
            role = role
        )        
        profile.save()        
        # Create Salesperson if Client
        return user        

class PublicUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only = True)
    salesperson = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email', 'role', 'salesperson')
    
    def get_role(self, obj):
        return obj.userprofile.role.role

    def get_salesperson(self, obj):
        try:
            return obj.salesperson.id
        except:    
            return ""