from django.db import models

from oauth import models as M


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ServiceCategory(BaseModel):
    name = models.CharField(max_length=20)
    image = models.CharField(max_length=255)


class Service(BaseModel):
    owner = models.ForeignKey(M.UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    details = models.TextField()
    price = models.IntegerField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    description = models.TextField()
    price = models.IntegerField()
    image = models.CharField(max_length=250, null=True)
    province = models.ForeignKey(
        M.Province, on_delete=models.SET_NULL, db_constraint=False
    )
    city = models.ForeignKey(M.City, on_delete=models.SET_NULL, db_constraint=False)


class ServiceQueue(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(M.UserProfile, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
