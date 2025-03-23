from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .services import StudentService
from rest_framework import status, generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny  
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from rest_framework.decorators import action


class StudentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  
    authentication_classes = [JWTAuthentication]
    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            # Add user_instance to the serializer's validated data
            validated_data = serializer.validated_data.copy()
            service = StudentService()
            student = service.add_student(validated_data)
            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def list(self, request):
        query = request.query_params.get('query', None)
        service = StudentService()
        students = service.list_students(query)
        return Response(StudentResponse(students, many=True).data)


    def retrieve(self, request, pk=None):
        service = StudentService()
        student = service.get_student_detail(pk)
        if student:
            return Response(StudentResponse(student).data)
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        service = StudentService()
        updated_data = request.data
        student = service.update_student(pk, updated_data)
        if student:
            return Response(StudentSerializer(student).data)
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        service = StudentService()
        result = service.delete_student(pk)
        if result:
            return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)




