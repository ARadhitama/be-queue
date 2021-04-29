from .base import Application, BaseError

from oauth.models import UserProfile

class UserApp(Application):
    def __init__(self, id):
        self.__id = id
    
    def get_data_obj(self):
        return UserProfile.objects.filter(id=self.__id).first()
    
