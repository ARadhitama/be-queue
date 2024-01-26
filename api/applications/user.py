from .base import Application, BaseError

from api import models as M
from api.applications.static import StaticApp
from oauth.models import UserProfile


class UserApp(Application):
    def __init__(self, id):
        self.id = id
        self.static = StaticApp()

    def get_data_obj(self):
        return UserProfile.objects.filter(id=self.id).first()

