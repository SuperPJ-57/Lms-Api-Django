from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['userId', 'user_name', 'email']

class RegistrationSerializer(serializers.Serializer):
    user_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
