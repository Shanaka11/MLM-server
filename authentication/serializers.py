from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, UserProfile


class UserSerializer(serializers.ModelSerializer):
    # Fetch Role from user profile as well
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'email')
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):

    role = RoleSerializer(UserProfile.role, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'