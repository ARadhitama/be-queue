from .base import Application, BaseError
from .user import UserApp

from api.db_manager import is_valid_category
from api.global_var import *
from api.models import Service, ServiceCategory

class ServiceApp(Application):
    def __init__(self, id):
        self.id = id
        self.user = UserApp(id)

    def create_service(self, data):
        valid_category = is_valid_category(data["category_id"])
        if not valid_category:
            raise BaseError("wrong_category")
        try:
            Service.objects.create(
                owner_id=self.id,
                **data
            )
        except Exception as e:
            print(e)
            raise BaseError(e)
    
    def get_service_detail_obj(self, service_id):
        return Service.objects.filter(id=service_id).first()

    def get_service_detail_dict(self, service_id):
        return Service.objects.filter(id=service_id).values().all()

    def get_all_service_owned_arr(self):
        try:
            service_arr = Service.objects.filter(user_id=self.__id).values().all()
        except Exception:
            raise BaseError(DB_ERROR)
        
        if not service_arr:
            raise BaseError("no_company")

        result = []

        for service in service_arr:
            service_data = {
                "service_id": service['id'],
                "service_name": service['name'],
                "service_image": service['image']
            }
            result.append(service_data)

        return result
