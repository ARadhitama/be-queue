from django.db import models

from oauth.models import District, UserProfile


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ServiceCategory(BaseModel):
    name = models.CharField(max_length=20)


class Service(BaseModel):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    address = models.TextField(null=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    description = models.TextField()
    price = models.IntegerField()
    image = models.CharField(max_length=250, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL)


class ServiceQueue(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
