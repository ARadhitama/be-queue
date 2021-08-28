from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from api.global_var import ACCOUNT_TYPE

class UserProfile(AbstractUser):
    date_joined = None
    first_name = None
    is_active = None
    is_staff = None
    is_superuser = None
    last_login = None
    last_name = None
    
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    kabupaten = models.IntegerField(default=0)
    kecamatan = models.IntegerField(default=0)
    kelurahan = models.IntegerField(default=0)
    status_ban = models.BooleanField(default=False)
    foto_ktp = models.CharField(max_length=250, blank=True, null=True)
    tipe_akun = models.CharField(choices=ACCOUNT_TYPE, max_length=10, default='personal')

    objects = UserManager()

    def __str__(self):
        return self.id