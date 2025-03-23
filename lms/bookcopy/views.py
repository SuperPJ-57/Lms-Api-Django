from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BookCopySerializer,BookCopyResponse
from rest_framework.response import Response
from .services import BookCopyService
from rest_framework import status

# Create your views here.

class BookCopyViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        data = request.data
        if not isinstance(data, dict):
            return Response({"error": "Invalid data. Expected a dictionary, but got {}.".format(type(data).__name__)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BookCopySerializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data.copy()
            service = BookCopyService()
            book_copy = service.add_book_copy(validated_data)
            if book_copy is None or (isinstance(book_copy, dict) and "error" in book_copy):
                return Response(book_copy, status=status.HTTP_400_BAD_REQUEST)
            #debug
            print(book_copy)
            return Response(BookCopyResponse(book_copy).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        service = BookCopyService()

        if pk is not None:
            book_copy = service.get_book_copy_detail(pk)
            if book_copy is None:
                return Response(book_copy, status=status.HTTP_404_NOT_FOUND)
            return Response(BookCopyResponse(book_copy).data)

        return Response({"error": "Book Copy ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request):
        service = BookCopyService()
        book_copies = service.list_book_copies()
        return Response(BookCopyResponse(book_copies, many=True).data)

    def update(self, request, pk=None):
        service = BookCopyService()
        book_copy = service.get_book_copy_detail(pk)
        if book_copy is None:
            return Response(book_copy, status=status.HTTP_404_NOT_FOUND)

        serializer = BookCopySerializer(book_copy, data=request.data, partial=True)
        if serializer.is_valid():
            updated_book_copy = service.update_book_copy(pk, serializer.validated_data)
            return Response(BookCopySerializer(updated_book_copy).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        service = BookCopyService()
        result = service.delete_book_copy(pk)
        if result is None:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_204_NO_CONTENT)