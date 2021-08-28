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
                user_id=self.__id,
                category_id=data['category_id'],
                name=data['service_name'],
                description=data['description'],
                price=data['price'],
                open_time=data['open_time'],
                close_time=data['close_time'],
                kabupaten_id=data['kabupaten_id'],
                kabupaten_name=data['kabupaten_name'],
                kecamatan_id=data['kecamatan_id'],
                kecamatan_name=data['kecamatan_name'],
                kelurahan_id=data['kelurahan_id'],
                kelurahan_name=data['kelurahan_name']
            )
            return True
        except Exception:
            raise BaseError(DB_ERROR)
    
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

    def get_all_service_on_location_arr(self, category_id, location_id, filter='kelurahan'):
        try:
            if filter == 'kabupaten':
                service_arr = Service.objects.filter(category_id=category_id, kabupaten_id=location_id).values().all()
            elif filter == 'kecamatan':
                service_arr = Service.objects.filter(category_id=category_id, kecamatan_id=location_id).values().all()
            elif filter == 'kelurahan':
                service_arr = Service.objects.filter(category_id=category_id, kelurahan_id=location_id).values().all()
        except Exception:
            raise BaseError("no_service")
    
        if not service_arr:
            raise BaseError("no_service")

        result = []

        for service in service_arr:

            service_data = {
                "service_id": service['id'],
                "service_name": service['name'],
                "service_image": service['image']
            }
            result.append(service_data)

        return result