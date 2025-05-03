from datetime import timedelta, timezone
from student.models import Student
from book.models import Book
from transaction.models import Transaction
from .models import OverdueBorrower 
from bookcopy.models import BookCopy
from django.utils import timezone  # Ensure this import is from Django
from user.models import User

class DashboardRepository:
    @staticmethod
    def get_total_students():
        return Student.objects.all().count()

    @staticmethod
    def get_total_books():
        return Book.objects.all().count()

    @staticmethod
    def get_total_transactions():
        return Transaction.objects.all().count()

    @staticmethod
    def get_borrowed_books_count():
        return Transaction.objects.filter(
            transaction_type='Borrow'
        ).count()

    @staticmethod
    def get_returned_books_count():
        return Transaction.objects.filter(
            transaction_type='Return', 
        ).count()
    
    @staticmethod
    def get_available_books_count():
        return BookCopy.objects.filter(
            is_available=True
        ).count()
    
    @staticmethod
    def get_total_faculty():
        return Student.objects.values('department').distinct().count()
    
    @staticmethod
    def get_user(username):
        return User.objects.get(user_name=username)

    @staticmethod
    def get_overdue_borrowers():
        overdue_borrowers = []
        transactions = Transaction.objects.filter(transaction_type="Borrow").exclude(status="completed")

        for transaction in transactions:
            overdue_date = transaction.due_date + timedelta(days=1)
        
            current_date = timezone.now().date()
            if current_date > overdue_date: 
                overdue_borrower,created = OverdueBorrower.objects.get_or_create(
                    student=transaction.student,
                    transaction=transaction,
                    book = transaction.book
                )
                overdue_borrowers.append(overdue_borrower)
                # Update the transaction status to 'Overdue'
                transaction.status = 'Overdue'
                transaction.save()

        return overdue_borrowers