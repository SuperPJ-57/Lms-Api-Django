from .repositories import BookRepository

class BookService:

    def __init__(self):
        self.repo = BookRepository()

    def add_book(self, book_data):
        return self.repo.create_book(book_data)
    
    def update_book(self, book_id, updated_data):
        # Fetch existing book details first
        book = self.repo.get_book_by_id(book_id)
        if not book:
            return {"error": "Book not found"}
        
        # Update the book details
        updated_book = self.repo.update_book(book_id, updated_data)
        return updated_book
    
    def get_book_detail(self, book_id):
        book = self.repo.get_book_by_id(book_id)
        if not book:
            return {"error": "Book not found"}
        return book
    
    def delete_book(self, book_id):
        book = self.repo.get_book_by_id(book_id)
        if not book:
            return {"error": "Book not found"}
        
        self.repo.delete_book(book_id)
        return {"message": "Book deleted successfully"}
    
    def list_books(self,query=None):
        return self.repo.get_all_books(query)