from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .services import UserService
from rest_framework import status, generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from rest_framework.decorators import action


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # Disable authentication for login view

    def post(self, request):
        service = UserService()
        result = service.login(request.data)
        if isinstance(result, dict) and "error" in result:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens (access and refresh tokens)
        refresh = RefreshToken.for_user(result)

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        tokenReponse = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return Response(tokenReponse, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    # Disable authentication for registration view
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # If the serializer is valid, register the user using the UserService
            service = UserService()
            user = service.register_user(serializer.validated_data)
            user_serializer = UserSerializer(user)

            # Return a success response with the user data
            return Response({"message": "User created successfully", "user": user_serializer.data}, status=status.HTTP_201_CREATED)

        # If there are validation errors, return a 400 response with the error details
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = [JWTAuthentication]

    def get(self, request, username=None):
        service = UserService()
        if username is None:
            user = service.get_all_users()
            user_serializer = UserSerializer(user, many=True)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        # If username is provided, fetch the specific user
        # Fetch the user by username
        user = service.get_user(username)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        service = UserService()
        updated_data = request.data
        user = service.update_user(request.user.id, updated_data)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        service = UserService()
        result = service.delete_user(request.user.id)
        if result:
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
