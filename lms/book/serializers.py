from rest_framework import serializers
from .models import Book

class BookResponse(serializers.ModelSerializer):
    book_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    author_id = serializers.IntegerField(source="author.author_id",read_only=True)
    genre = serializers.CharField(read_only=True)
    author_name = serializers.CharField(source="author.name",read_only=True)
    isbn = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author_id', 'genre','author_name','isbn','quantity']

class BookSerializer(serializers.ModelSerializer):
    #author_id = serializers.IntegerField(source="author.author_id")
    class Meta:
        model = Book
        fields = [ 'title', 'author', 'genre','isbn']