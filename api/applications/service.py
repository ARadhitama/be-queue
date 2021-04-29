from .base import Application, BaseError
from .user import UserApp

from api.global_var import *
from api.models import Service

class ServiceApp(Application):
    def __init__(self, id):
        self.__id = id
        self.__user = UserApp(id)

    def create_service(self, category_id, company_id, data):
        try:
            Service.objects.create(
                company_id=company_id,
                category_id=category_id,
                name=data['name'],
                deskripsi=data['deskripsi'],
                price=data['price'],
                open_time=data['open_time'],
                close_time=data['close_time']
            )
        except Exception:
            raise BaseError(DB_ERROR)
    
    def get_service_detail_obj(self, service_id):
        return Service.objects.filter(id=service_id).first()
    
    