from api.applications.base import BaseError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from api.applications.static import StaticApp
from api.db_manager import get_session, is_valid_category, json_response_error
from api.decorators import api_check_login, api_check_owner
from api.global_var import *
from api.applications.service import ServiceApp
from api.applications.user import UserApp

import json


class TestView(View):
    def get(self, request):
        return JsonResponse({}, safe=False)


class ProtectedView(View):
    decorators = [api_check_login]

    @method_decorator(decorators)
    def dispatch(self, request, user_data, *args, **kwargs):
        self.user = user_data
        return super().dispatch(request, user_data, *args, **kwargs)


class Info(ProtectedView):
    def get(self, request, *args, **kwargs):
        res = {
            "username": self.user["username"],
            "on_queue": UserApp(self.user["id"]).check_queue,
        }

        return JsonResponse(res, safe=False)


class ProvinceView(ProtectedView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {
                "Province": [
                    {
                        "name": p.name,
                    }
                    for p in StaticApp.get_provinces()
                ]
            }
        )


class CityView(ProtectedView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            province = data["province"]
        except Exception:
            return json_response_error(INVALID_PARAM)

        return JsonResponse(
            {
                "City": [
                    {
                        "name": c.name,
                    }
                    for c in StaticApp.get_cities(province)
                ]
            }
        )


class CategoryView(ProtectedView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {
                "Category": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "image": c.image,
                    }
                    for c in StaticApp.get_categories()
                ]
            }
        )


class Services(ProtectedView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            category = data.get("category", "Goverment")
            city = data.get("city", None)
            province = data.get("province", None)
        except Exception:
            return json_response_error(INVALID_PARAM)

        if city:
            res = StaticApp.get_services_by_city(category, city)
        elif province:
            res = StaticApp.get_services_by_province(category, province)
        else:
            res = StaticApp.get_services_by_categories(category)

        return JsonResponse(
            {
                "services": [
                    {
                        "id": s.id,
                        "name": s.name,
                        "image": s.image,
                    }
                    for s in res
                ]
            }
        )


class ServiceDetailsView(ProtectedView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            service_id = int(data.get("service_id"))
        except Exception:
            return json_response_error(INVALID_PARAM)

        res = StaticApp.get_service_details(service_id)
        return JsonResponse(
            {
                "category": res.category.name,
                "name": res.name,
                "details": res.details,
                "address": res.address,
                "price": res.price,
                "open_time": res.open_time,
                "close_time": res.close_time,
                "image": res.image,
                "province_name": res.province,
                "city": res.city,
                "current_queue_number": 70,  # TODO
            }
        )


class Queue(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            service_id = data["service_id"]
        except Exception:
            return json_response_error(INVALID_PARAM)
        res = UserApp(self.user["id"]).queue_to_service(service_id)
        return JsonResponse({"queue_num": res}, safe=False)


class CheckQueueView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            service_id = data["service_id"]
        except Exception:
            return json_response_error(INVALID_PARAM)

        res = UserApp(self.user["id"]).get_user_queue(service_id)

        return JsonResponse({"data": res}, safe=False)


class CancelQueueView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            return json_response_error(INVALID_PARAM)

        res = UserApp(self.user["id"]).cancel_queue()

        return JsonResponse({}, safe=False)


class CreateServiceView(ProtectedView):
    @method_decorator(api_check_owner)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except Exception as e:
            return json_response_error(INVALID_PARAM)

        try:
            ServiceApp(self.user["id"]).create_service(data)
        except Exception as e:
            return json_response_error(e.message)

        return JsonResponse({"message": "ok"})


class DeleteServiceView(ProtectedView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            service_id = int(data.get("service_id"))
        except Exception:
            return json_response_error(INVALID_PARAM)

        try:
            ServiceApp(self.user["id"]).delete_service(service_id)
        except Exception as e:
            return json_response_error(e.message)
        return JsonResponse({"message": "ok"})


class GetAllOwnedServiceView(View):
    def get(self, request):
        try:
            user_data = get_session(request.headers.get("authorization", None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        service_app = ServiceApp(user_data["id"])
        try:
            result = service_app.get_owned_services()
        except Exception as e:
            return json_response_error(e.message)

        return JsonResponse(result, safe=False)


# class QueueUserView(View):
#     # queue to a service
#     def post(self, request):
#         try:
#             user_data = get_session(request.headers.get("authorization", None))
#         except:
#             return json_response_error(NOT_LOGGED_IN)

#         try:
#             data = json.loads(request.body)
#             service_id = data["service_id"]
#         except Exception:
#             return json_response_error(INVALID_PARAM)

#         queue_app = QueueApp(user_data["id"])

#         try:
#             result = queue_app.queue_to_service(data["service_id"])
#         except Exception as e:
#             return json_response_error(e)

#         return JsonResponse({"queue_number": result})


# class QueueServiceView(View):  # DONE
#     # get current queue
#     def post(self, request):
#         try:
#             user_data = get_session(request.headers.get("authorization", None))
#         except:
#             return json_response_error(NOT_LOGGED_IN)

#         try:
#             data = json.loads(request.body)
#             service_id = data["service_id"]
#         except Exception:
#             return json_response_error(INVALID_PARAM)

#         queue_app = QueueApp(user_data["id"])

#         try:
#             result = queue_app.get_current_queue(data["service_id"])
#         except Exception as e:
#             return json_response_error(e)

#         return JsonResponse(result, safe=False)


class HistoryView(ProtectedView):
    def get(self, request):
        res = UserApp(self.user["id"]).history()
        return JsonResponse({"history": res})
