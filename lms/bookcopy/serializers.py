from rest_framework import serializers
from .models import BookCopy

class BookCopySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookCopy
        fields = ['barcode', 'book', 'is_available']
        

class BookCopyResponse(serializers.ModelSerializer):
    barcode = serializers.IntegerField(read_only=True)
    book_id = serializers.IntegerField(source="book.book_id",read_only=True)
    title = serializers.CharField(source="book.title",read_only=True)
    isbn = serializers.CharField(source="book.isbn",read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = BookCopy
        fields = ['barcode', 'book_id', 'title', 'isbn', 'is_available']