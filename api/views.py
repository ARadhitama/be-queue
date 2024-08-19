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


class ProvinceView(View):
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


class CityView(View):
    def get(self, request, *args, **kwargs):
        province = request.GET.get('province', "")
        if not province:
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
            category = request.GET.get('category', "")
            city = data.get("city", None)
            province = data.get("province", None)
        except Exception:
            return json_response_error(INVALID_PARAM)

        if city:
            res = StaticApp().get_services_by_city(category, city)
        elif province:
            res = StaticApp().get_services_by_province(category, province)
        else:
            res = StaticApp.get_services_by_categories(category)
        return JsonResponse(
            {
                "services": [
                    {
                        "service_id": s.id,
                        "service_name": s.name,
                        "service_image": s.image,
                        "is_open": s.is_open,
                        "category": s.category_id
                    }
                    for s in sorted(res, key=lambda x: x.is_open, reverse=True)
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
                "service_id": service_id,
                "category_id": res.category.id,
                "category_name": res.category.name,
                "name": res.name,
                "details": res.details,
                "address": res.address,
                "phone": res.phone,
                "price": res.price,
                "open_time": res.open_time,
                "close_time": res.close_time,
                "image": res.image,
                "province": res.province,
                "city": res.city,
                "current_queue_number": ServiceApp(self.user["id"]).get_current_queue(service_id)
            }
        )


class Queue(ProtectedView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            service_id = data["service_id"]
        except Exception:
            return json_response_error(INVALID_PARAM)
        
        try:
            res = ServiceApp(self.user["id"]).queue(service_id)
        except Exception as e:
            return json_response_error(e.message)
        return JsonResponse({}, safe=False)


class CheckQueueView(ProtectedView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"data": UserApp(self.user["id"]).get_user_queue()}, safe=False)


class CancelQueueView(ProtectedView):
    def get(self, request, *args, **kwargs):
        try:
            ServiceApp(self.user["id"]).cancel_queue()
        except Exception as e:
            return json_response_error(e.message)
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


class EditServiceView(ProtectedView):
    @method_decorator(api_check_owner)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except Exception as e:
            return json_response_error(INVALID_PARAM)

        try:
            ServiceApp(self.user["id"]).edit_service(data)
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


class GetAllOwnedServiceView(ProtectedView):
    def get(self, request, *args, **kwargs):
        try:
            result = ServiceApp(self.user["id"]).get_owned_services()
        except Exception as e:
            return json_response_error(e.message)

        return JsonResponse(result, safe=False)


class GetOwnedServiceDetailView(ProtectedView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            service_id = int(data.get("service_id"))
        except Exception:
            return json_response_error(INVALID_PARAM)

        try:
            result = ServiceApp(self.user["id"]).get_owned_service_detail(service_id)
        except Exception as e:
            return json_response_error(e.message)

        return JsonResponse(result, safe=False)


class ProcessQueueView(ProtectedView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            service_id = int(data.get("service_id"))
            action = data.get("action")
        except Exception:
            return json_response_error(INVALID_PARAM)

        try:
            ServiceApp(self.user["id"]).process_queue(service_id, action)
        except Exception as e:
            return json_response_error(e.message)

        return JsonResponse({}, safe=False)
    
    
class OpenService(ProtectedView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            service_id = int(data.get("service_id"))
        except Exception:
            return json_response_error(INVALID_PARAM)
        try:
            ServiceApp(self.user["id"]).open_service(service_id)
        except Exception as e:
            return json_response_error(e.message)
        return JsonResponse({"message": "ok"})


class CloseService(ProtectedView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            service_id = int(data.get("service_id"))
        except Exception:
            return json_response_error(INVALID_PARAM)
        try:
            ServiceApp(self.user["id"]).close_service(service_id)
        except Exception as e:
            return json_response_error(e.message)
        return JsonResponse({"message": "ok"})


class HistoryView(ProtectedView):
    def get(self, request, *args, **kwargs):
        res = UserApp(self.user["id"]).history()
        return JsonResponse({"history": res})
