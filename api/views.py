from api.applications.base import BaseError
from api.applications.queue import QueueApp
from django.db import reset_queries
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from api.applications.static import StaticApp
from api.db_manager import get_session, is_valid_category, json_response_error
from api.decorators import api_check_login
from api.global_var import *
from api.external_api.raja_api import *
from api.applications.service import ServiceApp

import json


class TestView(View):
    def get(self, request):
        return JsonResponse({}, safe=False)


class ProtectedView(View):
    decorators = [api_check_login]

    @method_decorator(decorators)
    def dispatch(self, request, user_data, *args, **kwargs):
        self.user = user_data
        return super().dispatch(request, *args, **kwargs)


class Info(ProtectedView):
    def get(self, request):
        res = {
            "username": self.user["username"],
            "on_queue": False,  # TODO
        }

        return JsonResponse(res, safe=False)


class ProvinceView(ProtectedView):
    def get(self, request):
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
    def post(self, request):
        try:
            data = json.loads(request.body)
            province = data["province"]
        except Exception:
            return json_response_error(INVALID_PARAM)

        return JsonResponse(
            {
                "Province": [
                    {
                        "name": c.name,
                    }
                    for c in StaticApp.get_cities(province)
                ]
            }
        )


class CategoryView(ProtectedView):
    def get(self, request):
        return JsonResponse(
            {
                "Category": [
                    {
                        "name": c.name,
                        "image": c.image,
                    }
                    for c in StaticApp.get_categories()
                ]
            }
        )


class Services(ProtectedView):
    def post(self, request):
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
                        "name": s.name,
                        "image": s.image,
                    }
                    for s in res
                ]
            }
        )


class ServiceDetailsView(ProtectedView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            service_id = int(data.get("service_id"))
        except Exception:
            return json_response_error(INVALID_PARAM)

        res = StaticApp.get_service_details(service_id)
        return JsonResponse(
            {
                "owner_name": res.owner.name,
                "category": res.category,
                "name": res.name,
                "details": res.details,
                "price": res.price,
                "open_time": res.open_time,
                "close_time": res.close_time,
                "image": res.image,
                "province_name": res.province.name,
                "city": res.city.name,
                "current_queue_served": 35,  # TODO,
                "current_queue_number": 70,  # TODO
            }
        )


# class CheckQueueView(View):
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
#             result = queue_app.get_user_queue(service_id)
#         except Exception as e:
#             return json_response_error(e)

#         return JsonResponse(result, safe=False)


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


# class GetAllOwnedServiceView(View):  # DONE
#     # get service based on company
#     def get(self, request):
#         try:
#             user_data = get_session(request.headers.get("authorization", None))
#         except:
#             return json_response_error(NOT_LOGGED_IN)

#         service_app = ServiceApp(user_data["id"])
#         try:
#             result = service_app.get_all_service_owned_arr()
#         except Exception as e:
#             return json_response_error(e.message)

#         return JsonResponse(result, safe=False)


# class CreateServiceView(View):  # DONE
#     # make new service, post category, ownner, company
#     def post(self, request):
#         try:
#             user_data = get_session(request.headers.get("authorization", None))
#         except:
#             return json_response_error(NOT_LOGGED_IN)

#         try:
#             data = json.loads(request.body)
#             category_id = (data["category_id"],)
#             service_name = (data["service_name"],)
#             description = (data["description"],)
#             price = (data["price"],)
#             open_time = (data["open_time"],)
#             close_time = (data["close_time"],)
#             kabupaten_id = (data["kabupaten_id"],)
#             kabupaten_name = (data["kabupaten_name"],)
#             kecamatan_id = (data["kecamatan_id"],)
#             kecamatan_name = (data["kecamatan_name"],)
#             kelurahan_id = (data["kelurahan_id"],)
#             kelurahan_name = (data["kelurahan_name"],)
#         except Exception:
#             return json_response_error(INVALID_PARAM)

#         # check valid category
#         valid_category = is_valid_category(data["category_id"])
#         if not valid_category:
#             return json_response_error("wrong_category")

#         created = False

#         service_app = ServiceApp(user_data["id"])
#         try:
#             created = service_app.create_service(data)
#         except Exception as e:
#             return json_response_error(e)

#         if created:
#             return JsonResponse({"message": SUCCESS})
#         else:
#             return json_response_error(DB_ERROR)
