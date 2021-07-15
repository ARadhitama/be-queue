from api.global_var import DB_ERROR
from api.models import ServiceQueue
from .base import Application, BaseError
from .user import UserApp

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