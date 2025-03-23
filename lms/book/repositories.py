from .models import Book
from django.db.models import Q

class BookRepository:

    def create_book(self, book_data):
        return Book.objects.create(**book_data)
    
    def get_book_by_id(self,book_id):
        book = Book.objects.filter(book_id = book_id, is_deleted = False).first()
        return book

    def get_all_books(self,query=None):
        books = Book.objects.filter(is_deleted = False)
        if query:
            books = Book.objects.filter(Q(title__icontains=query) )
        
        return books

    def update_book(self,book_id,updated_data):
        book = Book.objects.filter(book_id=book_id,is_deleted=False).first()
        if not book:
            return None
        
        for key,value in updated_data.items():
            setattr(book,key,value)

        book.save()


        return book
    
    def delete_book(self,book_id):
        book = Book.objects.filter(book_id=book_id,is_deleted=False).first()

        if not book:
            return None

        book.is_deleted = True

        book.save()

        return book 



    

