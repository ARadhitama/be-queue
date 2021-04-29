from django.db import models

from oauth.models import UserProfile

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ServiceCategory(models.Model):
    category = models.CharField(max_length=20)


class Company(BaseModel):
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    provinsi = models.CharField(max_length=20)
    kota = models.CharField(max_length=20)
    no_hp = models.CharField(max_length=20)
    deskripsi = models.TextField()
    

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
    deskripsi = models.TextField()
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
    number = models.IntegerField()


class QueueHistory(BaseModel):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    number = models.IntegerField()