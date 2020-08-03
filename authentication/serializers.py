from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    # Fetch Role from user profile as well
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email')