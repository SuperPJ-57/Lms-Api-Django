from django.db import models
from author.models import Author

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Books'
        indexes = [
            models.Index(fields=['title'], name='idx_books'),
        ]

    def __str__(self):
        return self.title
    