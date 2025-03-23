from django.contrib import admin
from .models import Author

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_id', 'name', 'bio', 'is_deleted', 'created_at', 'updated_at')
    search_fields = ('name', 'author_id')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Author, AuthorAdmin)