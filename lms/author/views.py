from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import AuthorSerializer
from rest_framework.response import Response
from .services import AuthorService
from rest_framework import status
from rest_framework.decorators import action

# Create your views here.


class AuthorViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            # Add user_instance to the serializer's validated data
            validated_data = serializer.validated_data.copy()
            service = AuthorService()
            author = service.add_author(validated_data)
            return Response(AuthorSerializer(author).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        service = AuthorService()

        if pk is not None:  # If an ID (pk) is provided, fetch a single author
            author = service.get_author_detail(pk)
            if not author:
                return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(AuthorSerializer(author).data)
        return Response({"error": "Author ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
    #list all authors
    
    def list(self, request):
        query = request.query_params.get('query', None)
        service = AuthorService()
        authors = service.list_authors(query)
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    


    def update(self, request, pk=None):
        service = AuthorService()

        # Ensure the author exists before updating
        author = service.get_author_detail(pk)
        if not author:
            return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorSerializer(
            author, data=request.data, partial=True)  # Supports partial updates
        if serializer.is_valid():
            updated_author = service.update_author(pk, serializer.validated_data)
            return Response(AuthorSerializer(updated_author).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        service = AuthorService()
        result = service.delete_author(pk)
        if result:
            return Response({"message": "Author deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
