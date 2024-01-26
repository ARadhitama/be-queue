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

    @property
    def check_queue(self):
        return M.ServiceQueue.objects.filter(user_id=self.id, completed=False).exists()

    def queue_to_service(self, service_id: int):
        if self.check_queue:
            raise BaseError("IN_QUEUE")
        service_status = M.ServiceStatus.objects.filter(service_id=service_id).last()
        if not service_status.is_open:
            raise BaseError("SERVICE_CLOSED")

        current_queue = (
            M.ServiceQueue.objects.filter(
                service_id=service_id, completed=False
            ).count()
            or 0
        )
        queue_number = current_queue + 1
        M.ServiceQueue.objects.create(
            service_id=service_id,
            user=self.__id,
            completed=False,
        )
        return queue_number

    def get_user_queue(self, service_id: int):
        if not self.check_queue:
            return

        service_queue = M.ServiceQueue.objects.filter(
            service_id=service_id, completed=False
        ).all()
        queue_num, queue_data = [
            (idx, queue)
            for idx, queue in enumerate(service_queue)
            if queue.user_id == self.id
        ][0]

        result = {
            "service_name": queue_data.service.name,
            "service_phone": queue_data.service.phone,
            "service_address": queue_data.service.address,
            "service_price": queue_data.service.price,
            "service_details": queue_data.service.details,
            "user_queue_number": queue_num,
        }

        return result

    def cancel_queue(self):
        if not self.check_queue:
            return

        queue = M.ServiceQueue.objects.filter(user_id=self.id, completed=False).last()

        queue.completed = True
        queue.save()
        return

    def history(self):
        history_list = M.ServiceQueue.objects.filter(user_id=self.id).all()

        res = []
        for h in history_list:
            res.append(
                {
                    "created_at": h.created_at,
                    "category": h.service.category,
                    "name": h.service.name,
                    "details": h.service.details,
                    "price": h.service.price,
                    "image": h.service.image,
                    "province_name": h.service.province.name,
                    "city": h.service.city.name,
                    "status": True if h.completed else False,
                }
            )

        return sorted(res, key=lambda item: item["created_at"], reverse=True)
