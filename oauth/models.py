from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class Province(models.Model):
    name = models.CharField(max_length=50)


class City(models.Model):
    province = models.ForeignKey(
        Province, on_delete=models.SET_NULL, db_constraint=False
    )
    name = models.CharField(max_length=50)



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
    password = models.CharField(max_length=255)
    province = models.ForeignKey(
        Province, on_delete=models.SET_NULL, db_constraint=False
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, db_constraint=False)

    objects = UserManager()

    def __str__(self):
        return self.id
