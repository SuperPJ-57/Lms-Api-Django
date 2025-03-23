from django.contrib import admin
from .models import BookCopy

# Register your models here.
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'book', 'is_available', 'is_deleted', 'created_at', 'updated_at')
    search_fields = ('book', 'barcode', )
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(BookCopy, BookCopyAdmin)
