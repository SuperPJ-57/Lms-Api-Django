from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, password=None, **extra_fields):
        """Create and return a regular user with a username and password."""
        if not user_name:
            raise ValueError("The Username field must be set")
        
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password=None,email=None, **extra_fields):
        """Create and return a superuser with given details."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_name, password,email, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.user_name
