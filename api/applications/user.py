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
        return M.ServiceQueue.objects.filter(user_id=self.id, completed=False).first()

    def get_user_queue(self):
        queue = self.check_queue
        if not queue:
            return

        service_queue = M.ServiceQueue.objects.filter(
            service_id=queue.service.id, completed=False
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
                    "category": h.service.category.name,
                    "name": h.service.name,
                    "details": h.service.details,
                    "price": h.service.price,
                    "image": h.service.image,
                    "province": h.service.province,
                    "city": h.service.city,
                    "status": h.status,
                }
            )

        return sorted(res, key=lambda item: item["created_at"], reverse=True)
