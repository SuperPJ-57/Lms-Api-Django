from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BookResponse, BookSerializer
from rest_framework.response import Response
from .services import BookService
from rest_framework import status

# Create your views here.


class BookViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # Add user_instance to the serializer's validated data
            validated_data = serializer.validated_data.copy()
            service = BookService()
            book = service.add_book(validated_data)
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self,request, pk=None):
        service = BookService()

        if pk is not None:  # If an ID (pk) is provided, fetch a single book
            book = service.get_book_detail(pk)
            if not book:
                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(BookResponse(book).data)

        return Response({"error": "Book ID not provided"}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        query = request.query_params.get('query', None)
        service = BookService()
        books = service.list_books(query)
        return Response(BookResponse(books, many=True).data)

    def update(self, request, pk=None):
        service = BookService()

        # Ensure the book exists before updating
        book = service.get_book_detail(pk)
        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(
            book, data=request.data, partial=True)  # Supports partial updates
        if serializer.is_valid():
            updated_book = service.update_book(pk, serializer.validated_data)
            return Response(BookSerializer(updated_book).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        service = BookService()
        result = service.delete_book(pk)
        if result:
            return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
