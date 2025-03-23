from .repositories import BookCopyRepository
from book.repositories import BookRepository

class BookCopyService:

    def __init__(self):
        self.repo = BookCopyRepository()
        self.book_repo = BookRepository()

    def add_book_copy(self, copy_data):
        book_id = copy_data.get("book").book_id
        book = self.book_repo.get_book_by_id(book_id)
        
        if not book:
            return {"error": "Book not found"}
        
        book.quantity += 1
        book.save()
        
        return self.repo.create_book_copy(copy_data)
    
    def update_book_copy(self, barcode, updated_data):
        # Fetch existing book copy details first
        book_copy = self.repo.get_book_copy_by_barcode(barcode)
        if not book_copy:
            return {"error": "Book copy not found"}
        
        # Update the book copy details
        updated_book_copy = self.repo.update_book_copy(barcode, updated_data)
        return updated_book_copy
    
    def get_book_copy_detail(self, barcode):
        book_copy = self.repo.get_book_copy_by_barcode(barcode)
        if not book_copy:
            return {"error": "Book copy not found"}
        return book_copy
    
    def delete_book_copy(self, barcode):
        book_copy = self.repo.get_book_copy_by_barcode(barcode)
        if not book_copy:
            return {"error": "Book copy not found"}
        
        book = self.book_repo.get_book_by_id(book_copy.book_id)
        if book:
            book.quantity -= 1
            book.save()
        
        self.repo.delete_book_copy(barcode)
        return {"message": "Book copy deleted successfully"}
    
    def list_book_copies(self):
        return self.repo.get_all_book_copies()
