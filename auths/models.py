import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from core.models import BaseDB
import uuid


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email=None, username=None, password=None):
        user = self.model(
            email=self.normalize_email(email), password=password, username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, password=None):
        """Creates and saves a superuser with the given email and password."""
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class Role(models.Model):
    role_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        db_table = "role_name"

    def __str__(self):
        return self.role_name

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=5000)
    username = models.CharField(max_length=255, unique=True)
    ####MIGRATING TO single user
    full_name = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=500, null=True)
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True, blank=True,related_name='userrole')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    class Meta:
        """Meta definition for User."""

        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

    def __str__(self):
        return self.username


class LoginLog(BaseDB):
    """Model definition for LoginLog."""

    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(auto_now=False, null=True, blank=True)

    class Meta:
        """Meta definition for LoginLog."""

        verbose_name = "LoginLog"
        verbose_name_plural = "LoginLogs"
        db_table = "login_log"

    def __str__(self):
        """Unicode representation of LoginLog."""
        return self.created_by.username





class Staff(BaseDB):
    full_name = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey("User", related_name="user", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=500, null=True)
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
        db_table = "staff"

    def __str__(self):
        return self.full_name


class DefaultPassword(BaseDB):
    password = models.CharField(max_length=50)

    class Meta:
        verbose_name = "DefaultPassword"
        verbose_name_plural = "DefaultPasswords"
        db_table = "default_password"

    def __str__(self):
        return self.name
