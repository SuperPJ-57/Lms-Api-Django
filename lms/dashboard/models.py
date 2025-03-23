from django.db import models
from student.models import Student
from book.models import Book
from transaction.models import Transaction
from user.models import User

class OverdueBorrower(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return "__all_"


class Dashboard(models.Model):
    total_borrowed_books = models.IntegerField()
    total_books = models.IntegerField()
    total_returned_books = models.IntegerField()
    total_user_base = models.IntegerField()
    total_books = models.IntegerField()
    available_books = models.IntegerField()
    total_faculty = models.IntegerField()
    # username = models.CharField(max_length=50)
    # user_id = models.IntegerField()
    # email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    