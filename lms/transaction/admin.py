from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'student', 'user', 'book', 'transaction_type', 'date', 'bookcopy', 'due_date', 'status')
    search_fields = ('student__name', 'book__title', 'transaction_id')
    list_filter = ('transaction_type', 'status', 'date', 'due_date')
    ordering = ('-date',)
    readonly_fields = ('transaction_id',)

admin.site.register(Transaction, TransactionAdmin)