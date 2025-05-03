from .models import Transaction
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'student', 'user','book','bookcopy','transaction_type','status']

class TransactionResponse(serializers.ModelSerializer):
    barcode = serializers.CharField(source='bookcopy.barcode')
    student_id = serializers.IntegerField(source='student.student_id')
    borrower_name = serializers.CharField(source='student.name')
    book_id = serializers.IntegerField(source='book.book_id')
    book_title = serializers.CharField(source='book.title')
    #user_id = serializers.IntegerField(source='user.userId')
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'student_id', 'borrower_name','book_id','book_title','barcode','transaction_type','status','date','due_date','user']