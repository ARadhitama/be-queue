from .base import Application, BaseError
from .user import UserApp

from api.db_manager import is_valid_category
from api.global_var import *
from api.models import Service, ServiceQueue


class ServiceApp(Application):
    def __init__(self, id):
        self.id = id
        self.user = UserApp(id)

    def create_service(self, data):
        valid_category = is_valid_category(data["category_id"])
        if not valid_category:
            raise BaseError("wrong_category")
        del data["current_queue_number"]
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
                "is_open": service["is_open"],
                "category": service["category_id"]
            }
            result.append(service_data)

        return sorted(result, key=lambda x: x["is_open"], reverse=True)
    
    def get_owned_service_detail(self, service_id: int):
        first_queue = ServiceQueue.objects.filter(service_id=service_id, completed=False).first()
        if not first_queue:
            return {}
        if first_queue.service.owner.id != self.id:
            raise BaseError("not_owner")
        queue_num = ServiceQueue.objects.filter(service_id=service_id, completed=False).count()
        return {
            "service_id": service_id,
            "service_name": first_queue.service.name,
            "customer_name": first_queue.user.username,
            "phone_number": first_queue.user.phone_number,
            "in_queue": queue_num
        }

    def open_service(self, service_id: int):
        service = Service.objects.filter(id=service_id).first()
        if not service:
            raise BaseError("service_not_found")
        if service.owner_id != self.id:
            raise BaseError("not_service_owner")
        service.is_open = True
        service.save()
    
    def close_service(self, service_id: int):
        service = Service.objects.filter(id=service_id).first()
        if not service:
            raise BaseError("service_not_found")
        if service.owner_id != self.id:
            raise BaseError("not_service_owner")
        service.is_open = False
        service.save()
        
    def queue(self, service_id: int):
        service = Service.objects.filter(id=service_id).first()
        if not service:
            raise BaseError("service_not_found")
        if not service.is_open:
            raise BaseError("service_not_open")
        if self.user.check_queue:
            raise BaseError("in_queue")
        
        ServiceQueue.objects.create(
            service_id=service_id,
            user=self.user.get_data_obj()
        )
        
    def cancel_queue(self):
        queue = self.user.check_queue
        if not queue:
            raise BaseError("not_in_queue")
        
        queue.completed = True
        queue.status = CANCELED
        queue.save()
    
    def get_current_queue(self, service_id: int):
        return ServiceQueue.objects.filter(service_id=service_id, completed=False).count()
    
    def process_queue(self, service_id: int, action: str):
        queue = ServiceQueue.objects.filter(service_id=service_id, completed=False).first()
        if not queue:
            raise BaseError("queue_not_found")
        if queue.service.owner.id != self.id:
            raise BaseError("not_owner")
        
        queue.completed = True
        queue.status = action
        queue.save()