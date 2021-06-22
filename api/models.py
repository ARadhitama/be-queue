from django.db import models

from oauth.models import UserProfile

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Provinsi(BaseModel):
    name = models.CharField(max_length=50)


class Kota(BaseModel):
    provinsi = models.ForeignKey(
        Provinsi,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)


class ServiceCategory(models.Model):
    category = models.CharField(max_length=20)


class Company(BaseModel):
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    address = models.TextField()
    kota = models.ForeignKey(
        Kota,
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    

class Service(BaseModel):
    company = models.ForeignKey(
        Company,
        to_field='id',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.IntegerField()
    open_time = models.TimeField()
    close_time = models.TimeField()


class ServiceQueue(BaseModel):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    number = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)