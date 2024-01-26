from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class Province(models.Model):
    name = models.CharField(max_length=50, unique=True)


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)


class UserProfile(AbstractUser):
    date_joined = None
    first_name = None
    is_active = None
    is_staff = None
    is_superuser = None
    last_login = None
    last_name = None
    email = None

    username = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    user_type = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.id
