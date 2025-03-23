from django.db import models
from book.models import Book

class BookCopy(models.Model):
    barcode = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'BookCopies'
        indexes = [
            models.Index(fields=['book'], name='idx_bookcopies'),
        ]

    def __str__(self):
        str = f'{self.barcode} - {self.book} - {self.is_available} - {self.is_deleted}'
        return str