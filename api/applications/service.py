from .base import Application, BaseError
from .user import UserApp

from api.global_var import *
from api.models import Service, ServiceCategory

class ServiceApp(Application):
    def __init__(self, id):
        self.__id = id
        self.__user = UserApp(id)

    def create_service(self, data):
        try:
            Service.objects.create(
                company_id=data['company_id'],
                category_id=data['category_id'],
                name=data['service_name'],
                description=data['description'],
                price=data['price'],
                open_time=data['open_time'],
                close_time=data['close_time']
            )
            return True
        except Exception:
            raise BaseError(DB_ERROR)
    
    def get_service_detail_obj(self, service_id):
        return Service.objects.filter(id=service_id).first()

    def get_service_detail_dict(self, service_id):
        return Service.objects.filter(id=service_id).values().all()

    def get_all_service_on_company_dict(self, company_id):
        return Service.objects.filter(company_id=company_id).values().all()

    def get_all_service_on_location_dict(self, kota):
        return Service.objects.filter(kota=kota).values().all()
    
    