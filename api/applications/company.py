from .base import Application, BaseError
from .user import UserApp

from api.global_var import *
from api.models import Company

class CompanyApp(Application):
    def __init__(self, id):
        self.__id = id
        self.__user = UserApp(id)

    def create_company(self, data):
        try:
            Company.objects.create(
                owner_id=self.__id,
                name=data['name'],
                description=data['description'],
                email=data['email'],
                kota=data['kota'],
                no_hp=data['no_hp']
            )
            return True
        except Exception:
            raise BaseError(DB_ERROR)
    
    def get_all_company_data_dict(self):
        return Company.objects.filter(owner_id=self.__id).values().all()
