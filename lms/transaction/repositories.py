from django.db import transaction
from .models import Transaction
from django.db.models import Q

class TransactionRepository:

    @transaction.atomic
    def create_transaction(self, transaction_data):
        """Creates a new transaction."""
        return Transaction.objects.create(**transaction_data)

    def get_transaction_by_id(self, transaction_id):
        """Retrieves a transaction by ID."""
        return Transaction.objects.filter(transaction_id=transaction_id).first()

    def get_transaction_by_barcode(self, barcode):
        """Retrieves a transaction by barcode whose status is 'Overdue' or 'Active'."""
        transaction =  Transaction.objects.filter(bookcopy__barcode=barcode, status__in=['Overdue', 'Active']).first()
        return transaction

    def get_transactions_by_student(self, student_id):
        """Retrieves all transactions for a specific student."""
        return Transaction.objects.filter(student_id=student_id)

    def get_all_transactions(self,query=None,completed=None):
        """Retrieves all transactions."""
        transactions = Transaction.objects.all() if completed else Transaction.objects.filter(status__in=['Active', 'Overdue'])
        if query:
            transactions = transactions.filter(
                Q(transaction_id__icontains=query) |
                Q(book__isbn__icontains=query) |
                Q(bookcopy__barcode__icontains=query) | 
                Q(student__name__icontains=query) |
                Q(transaction_type__icontains=query) |
                Q(status__icontains=query) |
                Q(date__icontains=query) |
                Q(due_date__icontains=query) |
                Q(book__title__icontains=query) |
                Q(user__user_name__icontains=query)             
            )
        return transactions

    @transaction.atomic
    def delete_transaction(self, transaction_id):
        """Deletes a transaction."""
        transaction_obj = self.get_transaction_by_id(transaction_id)
        if not transaction_obj:
            return None

        transaction_obj.delete()
        return transaction_obj