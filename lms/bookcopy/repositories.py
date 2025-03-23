from .models import BookCopy

class BookCopyRepository:
    
    def create_book_copy(self, copy_data):
        return BookCopy.objects.create(**copy_data)
    
    def get_book_copy_by_barcode(self, barcode):
        return BookCopy.objects.filter(barcode=barcode, is_deleted=False).first()

    def get_all_book_copies(self, query=None):
        return BookCopy.objects.filter(is_deleted=False)

    def update_book_copy(self, barcode, updated_data):
        book_copy = BookCopy.objects.filter(barcode=barcode, is_deleted=False).first()
        if not book_copy:
            return None
        
        for key, value in updated_data.items():
            setattr(book_copy, key, value)
        
        book_copy.save()
        return book_copy
    
    def delete_book_copy(self, barcode):
        book_copy = BookCopy.objects.filter(barcode=barcode, is_deleted=False).first()
        if not book_copy:
            return None
        
        book_copy.is_deleted = True
        book_copy.save()
        return book_copy
