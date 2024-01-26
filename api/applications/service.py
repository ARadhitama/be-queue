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
            Service.objects.create(owner_id=self.id, **data)
        except Exception as e:
            raise BaseError(e)
        return

    def edit_service(self, data):
        service = Service.objects.filter(id=data.get("service_id")).first()
        if not service:
            raise BaseError("service_not_found")
        if service.owner_id != self.id:
            raise BaseError("not_service_owner")

        for key, value in data.items():
            setattr(service, key, value)
        service.save()
        return

    def delete_service(self, service_id: int):
        service = Service.objects.filter(id=service_id).first()
        if not service:
            raise BaseError("service_not_found")
        if service.owner_id != self.id:
            raise BaseError("not_service_owner")
        service.delete()

    def get_owned_services(self):
        try:
            service_list = Service.objects.filter(owner_id=self.id).values().all()
        except Exception:
            raise BaseError(DB_ERROR)

        result = []
        for service in service_list:
            service_data = {
                "service_id": service["id"],
                "service_name": service["name"],
                "service_image": service["image"],
            }
            result.append(service_data)

        return result
