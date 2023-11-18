from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from api.global_var import ACCOUNT_TYPE


class Province(models.Model):
    name = models.CharField(max_length=50)


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class District(models.Model):
    City = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


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
    phone_number = models.CharField(max_length=20)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    type = models.CharField(choices=ACCOUNT_TYPE, max_length=10, default="personal")

    objects = UserManager()

    def __str__(self):
        return self.id
