from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class UserProfile(AbstractUser):
    date_joined = None
    first_name = None
    is_active = None
    is_staff = None
    is_superuser = None
    last_login = None
    last_name = None

    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=50)
    provinsi = models.CharField(max_length=20)
    kota = models.CharField(max_length=20)
    status_ban = models.BooleanField(default=False)
    foto_ktp = models.CharField(max_length=250, blank=True, null=True)
    is_customer = models.BooleanField(default=True)

    objects = UserManager()

    def __str__(self):
        return self.id
