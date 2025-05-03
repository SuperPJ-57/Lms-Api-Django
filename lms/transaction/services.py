from django.utils import timezone
from .models import Transaction
from bookcopy.models import BookCopy
from user.models import User
from student.models import Student
from book.models import Book
from .repositories import TransactionRepository
from django.db import transaction

class TransactionService:
    def __init__(self):
        self.repo = TransactionRepository()

    @transaction.atomic
    def borrow_book(self, transaction_data):
        """Handle the borrowing of a book."""
        student = Student.objects.get(student_id=transaction_data['student'])
        user = User.objects.get(userId=transaction_data['user'])
        book = Book.objects.get(book_id=transaction_data['book'])
        book_copy = BookCopy.objects.get(barcode=transaction_data['bookcopy'], is_available=True)
        
        if not book_copy:
            return {"error": "No available copy to borrow"}

        # Create transaction
        # Create transaction
        transaction_data['student'] = student
        transaction_data['user'] = user
        transaction_data['book'] = book
        transaction_data['bookcopy'] = book_copy
        transaction_data['status'] = 'Active'
        transaction_data['transaction_type'] = 'Borrow'
        if transaction_data['date'] is None or transaction_data['date'] == '':
            transaction_data['date'] = timezone.now().date()
        else:
            transaction_data['date'] = transaction_data['date']
        transaction_data['due_date'] = (timezone.now() + timezone.timedelta(days=14)).date()  # Set due date (e.g., 14 days)

        transaction = self.repo.create_transaction(transaction_data)

        # Update book copy status
        book_copy.is_available = False
        book_copy.save()

        return transaction

    @transaction.atomic
    def return_book(self, transaction_data):
        """Handle the borrowing of a book."""
        # student = Student.objects.get(student_id=transaction_data['student'])
        # user = User.objects.get(userId=transaction_data['user'])
        # book = Book.objects.get(book_id=transaction_data['book'])
        # book_copy = BookCopy.objects.get(barcode=transaction_data['bookcopy'], is_available=False)
        # if not book_copy:
        #     return {"error": "The book is already returned"}
        

        transaction = self.repo.get_transaction_by_barcode(transaction_data['bookcopy'])
        book_copy = BookCopy.objects.get(barcode=transaction_data['bookcopy'])
        student = Student.objects.get(student_id=transaction.student.student_id)

        if not transaction:
            return {"error": "Transaction not found"}

        if transaction_data['student'] != student.student_id:
            return {"error": "The student is not the borrower of the book"}
        
        

        

        # Create transaction
        # Create transaction
        transaction_data['student'] = transaction.student
        transaction_data['user'] = transaction.user
        transaction_data['book'] = transaction.book
        transaction_data['bookcopy'] = transaction.bookcopy
        transaction_data['status'] = 'Completed'
        transaction_data['transaction_type'] = 'Return'
        transaction_data['date'] = timezone.now().date()
        transaction_data['due_date'] = transaction.due_date
        
        transaction = self.repo.create_transaction(transaction_data)

        transaction.status = 'Completed'
        transaction.save()

        # Update book copy status
        book_copy.is_available = True
        book_copy.save()

        return transaction


    # def return_book(self, student_id, transaction_id):
    #     """Handle the return of a book."""
    #     transaction = self.repo.get_transaction_by_id(transaction_id)
    #     if not transaction or transaction.student.student_id != student_id:
    #         return {"error": "Transaction not found"}

    #     # Update transaction status to 'Completed'
    #     transaction.status = 'Completed'
    #     transaction.save()

    #     # Update book copy status to available
    #     book_copy = BookCopy.objects.get(id=transaction.bookcopy.id)
    #     book_copy.is_available = True
    #     book_copy.save()

    #     return transaction

    def update_book_status_on_due(self):
        """Update the status of overdue books."""
        now = timezone.now()
        overdue_transactions = Transaction.objects.filter(due_date__lt=now, status='Active')

        for transaction in overdue_transactions:
            # Update status to 'Overdue'
            transaction.status = 'Overdue'
            transaction.save()

        return overdue_transactions