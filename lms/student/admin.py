from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email','contact_number','department','created_date', 'updated_date', 'is_deleted')
    search_fields = ('name', 'email')
    list_filter = ('is_deleted', 'created_date', 'updated_date')
    ordering = ('-created_date',)
    readonly_fields = ('created_date', 'updated_date')

admin.site.register(Student, StudentAdmin)