from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author','genre','isbn','quantity', 'is_deleted', 'created_at', 'updated_at')
    search_fields = ('title', 'book_id', 'author__name')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Book, BookAdmin)
