from django.db import models
from student.models import Student
from book.models import Book
from bookcopy.models import BookCopy
from user.models import User

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Overdue', 'Overdue'),
    ]
    TRANSACTION_TYPE_CHOICES = [
        ('Borrow', 'Borrow'),
        ('Return', 'Return'),
    ]

    transaction_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateField()
    bookcopy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'Transactions'
        indexes = [
            models.Index(fields=['transaction_type', 'student', 'status'], name='idx_transactions'),
        ]

    def __str__(self):
        transaction = f'{self.transaction_id} - {self.student} - {self.book} - {self.transaction_type} - {self.date} - {self.bookcopy} - {self.due_date} - {self.status}'
        return transaction