from rest_framework import serializers
from .models import Dashboard, OverdueBorrower

class OverdueBorrowerSerializer(serializers.ModelSerializer):
    borrower_id = serializers.CharField(source="student.student_id", read_only=True)
    borrow_id = serializers.CharField(source="transaction.transaction_id", read_only=True)
    borrower_name = serializers.CharField(source="student.name", read_only=True)
    borrower_email = serializers.EmailField(source="student.email", read_only=True)
    due_date = serializers.DateField(source="transaction.due_date", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = OverdueBorrower
        fields = ["borrower_id", "borrow_id","borrower_name","borrower_email","due_date","book_title"]
        
class DashboardSerializer(serializers.ModelSerializer):   


    total_borrowed_books = serializers.IntegerField()
    total_books = serializers.IntegerField()
    total_returned_books = serializers.IntegerField()
    total_user_base = serializers.IntegerField()
    total_books = serializers.IntegerField()
    available_books = serializers.IntegerField()
    total_faculty = serializers.IntegerField()
    user_name = serializers.CharField(source="user.user_name", read_only=True)
    user_id = serializers.CharField(source="user.userId", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    overdue_borrowers = OverdueBorrowerSerializer(many=True, read_only=True)


    class Meta:
        model = Dashboard
        fields = ["total_borrowed_books", "total_books", "total_returned_books", "total_user_base", "total_books", "available_books", "total_faculty", "user_name", "user_id", "email", "overdue_borrowers"]
