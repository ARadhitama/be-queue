from api.global_var import DB_ERROR
from api.models import ServiceQueue
from oauth.models import UserProfile
from .base import Application, BaseError
from .user import UserApp
from .service import ServiceApp

class QueueApp(Application):
    def __init__(self, id):
        self.__id = id
        self.__user = UserApp(id)

    def check_queue(self, service_id):
        try:
            queue = ServiceQueue.objects.filter(service_id=service_id, user_id=self.__id, completed=False).last()
        except Exception:
            raise BaseError(DB_ERROR)
        
        if queue:
            return True
        return False

    def get_current_queue(self, service_id):
        try:
            queue = ServiceQueue.objects.filter(service_id=service_id, completed=False).last()
            user_data = UserProfile.objects.filter(id=queue.user_id).first()
        except Exception:
            raise BaseError(DB_ERROR)

        result = {
            "queue_id": queue.id,
            "foto_ktp": user_data.foto_ktp,
            "queue_number": queue.number
        }
        
        return result

    def get_user_queue(self, service_id):
        try:
            user_queue_data = ServiceQueue.objects.filter(service_id=service_id, user_id=self.__id, completed=False).last()
            current_queue_data = ServiceQueue.objects.filter(service_id=service_id, completed=False).last()
        except Exception:
            raise BaseError(DB_ERROR)
        
        service_app = ServiceApp(self.__id)

        try:
            service_data = service_app.get_service_detail_obj(service_id)
        except Exception:
            raise BaseError(DB_ERROR)
        
        result = {
            "service_name": service_data.name,
            "service_phone": service_data.company_name,
            "service_address": service_data.address,
            "service_price": service_data.price,
            "service_description": service_data.description,
            "current_queue_number": current_queue_data.number,
            "user_queue_number": user_queue_data.number,
        }

        return result

    def queue_to_service(self, service_id):
        try:
            queue_data = ServiceQueue.objects.filter(service_id=service_id).last()
        except Exception:
            raise BaseError(DB_ERROR)

        queue_number = queue_data.number + 1

        try:
            ServiceQueue.objects.create(
                service_id=service_id,
                user=self.__id,
                number=queue_data.number + 1,
                completed=False
            )
        except Exception:
            raise BaseError(DB_ERROR)

        return queue_number