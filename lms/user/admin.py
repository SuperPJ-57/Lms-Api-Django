from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('userId', 'user_name', 'email', 'created_date', 'updated_date', 'is_deleted')
    search_fields = ('user_name', 'email')
    list_filter = ('is_deleted', 'created_date', 'updated_date')
    ordering = ('-created_date',)

admin.site.register(User, UserAdmin)