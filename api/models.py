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
    address = models.TextField()
    kabupaten_id = models.IntegerField(default=0)
    kabupaten_name = models.CharField(max_length=50, null=True)
    kecamatan_id = models.IntegerField(default=0)
    kecamatan_name = models.CharField(max_length=50, null=True)
    kelurahan_id = models.IntegerField(default=0)
    kelurahan_name = models.CharField(max_length=50, null=True)
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
    address = models.TextField(null=True)
    image = models.CharField(max_length=250, null=True)
    kabupaten_id = models.IntegerField(default=0)
    kabupaten_name = models.CharField(max_length=50, null=True)
    kecamatan_id = models.IntegerField(default=0)
    kecamatan_name = models.CharField(max_length=50, null=True)
    kelurahan_id = models.IntegerField(default=0)
    kelurahan_name = models.CharField(max_length=50, null=True)

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